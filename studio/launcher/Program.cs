using System.Diagnostics;
using System.IO.Compression;
using System.Reflection;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Text.Json;

internal static class Program
{
    [DllImport("user32.dll", CharSet = CharSet.Unicode)]
    private static extern int MessageBoxW(IntPtr window, string text, string title, uint type);

    private static int Main(string[] args)
    {
        // Test runs never read or write normal user state/cache.
        bool windowTest = args.Contains("--launcher-window-self-test");
        var testIndex = Array.IndexOf(args, windowTest ? "--launcher-window-self-test" : "--launcher-self-test");
        string? report = testIndex >= 0 && args.Length > testIndex + 1 ? Path.GetFullPath(args[testIndex + 1]) : null;
        try
        {
            if (testIndex >= 0 && report == null) throw new ArgumentException("Self-test requires a report path.");
            var home = testIndex >= 0
                ? Path.Combine(Path.GetDirectoryName(report!)!, "launcher-test-data")
                : Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "NebulithStudio");
            Directory.CreateDirectory(home);
            using var stream = Assembly.GetExecutingAssembly().GetManifestResourceStream("Nebulith.Payload")
                ?? throw new InvalidOperationException("Bundled application is missing.");
            string digest = Convert.ToHexString(SHA256.HashData(stream)).ToLowerInvariant();
            stream.Position = 0;
            var runtimeParent = Path.Combine(home, "runtime");
            Directory.CreateDirectory(runtimeParent);
            var target = Path.Combine(runtimeParent, digest);
            // Serialize extraction across launches, without requiring administrator access.
            using (var extractionLock = new Mutex(false, @"Local\NebulithStudio-" + digest))
            {
                bool owned;
                try { owned = extractionLock.WaitOne(TimeSpan.FromMinutes(2)); }
                catch (AbandonedMutexException) { owned = true; }
                if (!owned) throw new IOException("Application extraction is busy. Try again shortly.");
                try
                {
                    if (!Directory.Exists(target))
                    {
                        var stage = Path.Combine(runtimeParent, digest + "." + Guid.NewGuid().ToString("N"));
                        Directory.CreateDirectory(stage);
                        try
                        {
                            using var zip = new ZipArchive(stream, ZipArchiveMode.Read, leaveOpen: true);
                            zip.ExtractToDirectory(stage);
                            Validate(stage);
                            Directory.Move(stage, target);
                        }
                        finally { if (Directory.Exists(stage)) Directory.Delete(stage, true); }
                    }
                    Validate(target);
                }
                finally { extractionLock.ReleaseMutex(); }
            }
            var info = new ProcessStartInfo(Path.Combine(target, "runtime", "bin", "java.exe"))
            {
                UseShellExecute = false, CreateNoWindow = true,
                RedirectStandardOutput = true, RedirectStandardError = true,
                WorkingDirectory = target,
                StandardOutputEncoding = System.Text.Encoding.UTF8,
                StandardErrorEncoding = System.Text.Encoding.UTF8
            };
            info.ArgumentList.Add("-Dfile.encoding=UTF-8");
            info.ArgumentList.Add("-Dnebulith.dataDir=" + home);
            if (testIndex >= 0 && !windowTest) info.ArgumentList.Add("-Djava.awt.headless=true");
            info.ArgumentList.Add("-jar"); info.ArgumentList.Add(Path.Combine(target, "NebulithStudio.jar"));
            if (testIndex >= 0)
            {
                info.ArgumentList.Add(windowTest ? "--window-self-test" : "--self-test");
                info.ArgumentList.Add(Path.Combine(Path.GetDirectoryName(report!)!, windowTest ? "native-window" : "packaged-ui.png"));
            }
            else foreach (var arg in args) info.ArgumentList.Add(arg);
            using var process = Process.Start(info) ?? throw new IOException("Cannot start the bundled runtime.");
            var stdout = process.StandardOutput.ReadToEndAsync();
            var stderr = process.StandardError.ReadToEndAsync();
            process.WaitForExit(); Task.WaitAll(stdout, stderr);
            if (report != null)
                File.WriteAllText(report, JsonSerializer.Serialize(new {
                    payloadSha256 = digest, cache = target, runtime = info.FileName,
                    javaExitCode = process.ExitCode, stdout = stdout.Result, stderr = stderr.Result,
                    noSystemJavaRequired = true
                }, new JsonSerializerOptions { WriteIndented = true }));
            if (process.ExitCode != 0) throw new IOException("Studio failed to start.\n" + stderr.Result);
            return process.ExitCode;
        }
        catch (Exception error)
        {
            if (report != null) File.WriteAllText(report, JsonSerializer.Serialize(new { error = error.ToString() }));
            else MessageBoxW(IntPtr.Zero, error.Message, "Nebulith Studio", 0x10);
            return 1;
        }
    }

    private static void Validate(string root)
    {
        var files = JsonSerializer.Deserialize<Dictionary<string, string>>(File.ReadAllText(Path.Combine(root, "files.json")))!;
        foreach (var (relative, expected) in files)
        {
            var path = Path.GetFullPath(Path.Combine(root, relative));
            if (!path.StartsWith(Path.GetFullPath(root) + Path.DirectorySeparatorChar, StringComparison.OrdinalIgnoreCase))
                throw new IOException("Invalid application resource path.");
            using var file = File.OpenRead(path);
            if (!Convert.ToHexString(SHA256.HashData(file)).Equals(expected, StringComparison.OrdinalIgnoreCase))
                throw new IOException("Bundled file changed or is incomplete: " + relative);
        }
    }
}
