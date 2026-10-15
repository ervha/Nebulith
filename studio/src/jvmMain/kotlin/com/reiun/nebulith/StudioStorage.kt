package com.reiun.nebulith

import java.nio.channels.FileChannel
import java.nio.file.*
import java.util.Properties

data class StudioState(val dark: Boolean=false, val previewSize: Int=42, val divider: Double=.38,
    val draft: String="Falun el vyrin.", val favorites: Set<Int> = emptySet(), val history: List<Int> = emptyList(),
    val translationSource: String="",val translationFromNrs: Boolean=false)

/** Per-user local state, atomically replaced; a second process cannot overwrite it. */
class StudioStorage(val directory: Path = defaultDirectory()): AutoCloseable {
    private val file=directory.resolve("studio.properties")
    private val channel: FileChannel
    private val lock: java.nio.channels.FileLock
    var loadProblem: String?=null
        private set
    init {
        Files.createDirectories(directory)
        channel=FileChannel.open(directory.resolve("studio.lock"),StandardOpenOption.CREATE,StandardOpenOption.WRITE)
        lock=try { channel.tryLock() ?: throw IllegalStateException("Studioは既に起動しています。") }
            catch(e: Exception) { channel.close(); throw e }
    }
    fun load(): StudioState {
        if(!Files.exists(file)) return StudioState()
        return try {
            val p=Properties(); Files.newBufferedReader(file,Charsets.UTF_8).use { p.load(it) }
            check(p.getProperty("schema")=="1") { "未対応の保存形式" }
            val size=p.getProperty("previewSize").toInt(); check(size in 24..64)
            val divider=p.getProperty("divider").toDouble(); check(divider.isFinite() && divider in .15.. .85)
            val dark=p.getProperty("dark"); check(dark=="true" || dark=="false")
            val translationFromNrs=p.getProperty("translationFromNrs","false");check(translationFromNrs in listOf("true","false"))
            fun ids(key: String)=p.getProperty(key,"").split(',').filter { it.isNotBlank() }.map { it.toInt() }.filter { it in 1..1008 }.distinct()
            StudioState(dark.toBoolean(),size,divider,checkNotNull(p.getProperty("draft")),ids("favorites").toSet(),ids("history").take(50),
                p.getProperty("translationSource",""),translationFromNrs.toBoolean())
        } catch(e: Exception) {
            loadProblem="保存データを読み込めません。元ファイルは変更しません: ${file.toAbsolutePath()}"
            StudioState()
        }
    }
    fun save(state: StudioState) {
        check(loadProblem==null) { loadProblem ?: "読み込みエラー" }
        val p=Properties().apply {
            setProperty("schema","1"); setProperty("dark",state.dark.toString())
            setProperty("previewSize",state.previewSize.toString()); setProperty("divider",state.divider.toString())
            setProperty("draft",state.draft); setProperty("favorites",state.favorites.sorted().joinToString(","))
            setProperty("history",state.history.distinct().take(50).joinToString(","))
            setProperty("translationSource",state.translationSource);setProperty("translationFromNrs",state.translationFromNrs.toString())
        }
        val temp=Files.createTempFile(directory,"studio-",".tmp")
        try {
            Files.newBufferedWriter(temp,Charsets.UTF_8).use { p.store(it,"Nebulith Studio local state") }
            FileChannel.open(temp,StandardOpenOption.WRITE).use { it.force(true) }
            // Keep the previous complete save as a recovery copy.
            if(Files.exists(file)) Files.copy(file,directory.resolve("studio.properties.bak"),StandardCopyOption.REPLACE_EXISTING)
            try { Files.move(temp,file,StandardCopyOption.ATOMIC_MOVE,StandardCopyOption.REPLACE_EXISTING) }
            catch(_: AtomicMoveNotSupportedException) { Files.move(temp,file,StandardCopyOption.REPLACE_EXISTING) }
        } finally { Files.deleteIfExists(temp) }
    }
    override fun close() { lock.release(); channel.close() }
    companion object {
        fun defaultDirectory(): Path = Paths.get(System.getProperty("nebulith.dataDir") ?: (
            System.getenv("LOCALAPPDATA")?.let { "$it/NebulithStudio" } ?: "${System.getProperty("user.home")}/.nebulith-studio"))
    }
}
