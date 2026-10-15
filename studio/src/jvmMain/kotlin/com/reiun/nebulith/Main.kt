package com.reiun.nebulith

import java.awt.*
import java.awt.datatransfer.StringSelection
import java.awt.image.BufferedImage
import java.io.File
import java.util.Base64
import javax.imageio.ImageIO
import javax.swing.*
import javax.swing.event.DocumentEvent
import javax.swing.event.DocumentListener
import javax.swing.table.AbstractTableModel

object Bundle {
    private fun resource(name: String) = checkNotNull(Bundle::class.java.getResourceAsStream("/$name")) { "Missing bundled resource: $name" }
    private fun lines(name: String) = resource(name).bufferedReader(Charsets.UTF_8).use { it.readLines() }
    private fun decode(value: String) = String(Base64.getDecoder().decode(value), Charsets.UTF_8)
    val entries: List<Entry> by lazy {
        lines("lexicon.tsv").filter { !it.startsWith("#") && it.isNotBlank() }.map { line ->
            val cells = line.split('\t'); check(cells.size == 8)
            val s = cells.drop(1).map(::decode)
            Entry(cells[0].toInt(), s[0], s[1], s[2], s[3], s[4], s[5], s[6])
        }
    }
    val examples: List<Example> by lazy {
        lines("corpus.tsv").filter { it.isNotBlank() }.map { line ->
            val s = line.split('\t').map(::decode); check(s.size == 5)
            Example(s[0], s[1], s[2], s[3], s[4])
        }
    }
    val font: Font by lazy { resource("Nebulith-Regular.ttf").use { Font.createFont(Font.TRUETYPE_FONT, it) } }
    val characters: String by lazy { resource("characters.txt").bufferedReader(Charsets.UTF_8).use { it.readText() } }
    val version: String by lazy { resource("version.txt").bufferedReader(Charsets.UTF_8).use { it.readText().trim() } }
}

class WordsModel : AbstractTableModel() {
    var rows = Bundle.entries
        set(value) { field = value; fireTableDataChanged() }
    override fun getRowCount() = rows.size
    override fun getColumnCount() = 3
    override fun getColumnName(column: Int) = listOf("NRS", "意味", "品詞")[column]
    override fun getValueAt(row: Int, column: Int): Any = when(column) {
        0 -> rows[row].nrs; 1 -> rows[row].meaningJa; else -> rows[row].pos
    }
}

fun JTextArea.readOnly() = apply { isEditable = false; lineWrap = true; wrapStyleWord = true; border = BorderFactory.createEmptyBorder(12,12,12,12) }
fun onChange(component: javax.swing.text.JTextComponent, action: () -> Unit) {
    component.document.addDocumentListener(object : DocumentListener {
        override fun insertUpdate(e: DocumentEvent) = action()
        override fun removeUpdate(e: DocumentEvent) = action()
        override fun changedUpdate(e: DocumentEvent) = action()
    })
}

class StudioPanel : JPanel(BorderLayout(16,16)) {
    val query = JTextField()
    val editor = JTextArea("Falun el vyrin.", 3, 30)
    val preview = JTextArea().readOnly()
    val model = WordsModel()
    private val table = JTable(model)
    private val details = JTextArea().readOnly()
    private val wordPreview = JTextArea().readOnly()
    private val count = JLabel()
    private val categories = JComboBox((listOf("全カテゴリー") + Bundle.entries.map { it.category }.distinct()).toTypedArray())
    private val status = JLabel("入力はこの画面内だけに保持します。終了後には保存されません。")

    init {
        border = BorderFactory.createEmptyBorder(20,20,20,20)
        background = Color(242,245,247)
        val header = JPanel(BorderLayout()).apply { isOpaque = false }
        header.add(JLabel("NEBULITH  /  星辰語スタジオ").apply { font = font.deriveFont(Font.BOLD,22f) }, BorderLayout.WEST)
        header.add(JLabel("オフライン辞書 · ${Bundle.entries.size}語").apply { foreground = Color(80,100,118) }, BorderLayout.EAST)
        add(header, BorderLayout.NORTH)
        val search = JPanel(GridLayout(0,1,0,8)).apply {
            isOpaque = false
            add(JLabel("辞書を検索 — 語幹・意味・IPA・ID")); add(query); add(categories); add(count)
        }
        query.toolTipText = "複数語は空白で区切って絞り込みます"
        val left = JPanel(BorderLayout(0,12)).apply { isOpaque = false; add(search,BorderLayout.NORTH) }
        table.rowHeight = 34; table.setSelectionMode(ListSelectionModel.SINGLE_SELECTION)
        table.fillsViewportHeight = true
        table.columnModel.getColumn(0).preferredWidth = 110
        table.columnModel.getColumn(1).preferredWidth = 270
        table.columnModel.getColumn(2).preferredWidth = 45
        left.add(JScrollPane(table),BorderLayout.CENTER)
        val tabs = JTabbedPane()
        wordPreview.font = Bundle.font.deriveFont(64f)
        wordPreview.preferredSize = Dimension(400,130)
        val wordPanel = JPanel(BorderLayout(0,12))
        wordPanel.add(wordPreview,BorderLayout.NORTH)
        wordPanel.add(JScrollPane(details),BorderLayout.CENTER)
        val insert = JButton("選択した語を入力欄へ追加")
        insert.addActionListener {
            val selected = model.rows.getOrNull(table.selectedRow)
            if (selected != null) {
                editor.replaceSelection(selected.nrs)
                tabs.selectedIndex = 1
            }
        }
        wordPanel.add(insert,BorderLayout.SOUTH)
        tabs.addTab("語の詳細",wordPanel)
        editor.font = Font(Font.MONOSPACED,Font.PLAIN,18); editor.lineWrap = true; editor.wrapStyleWord = true
        editor.border = BorderFactory.createEmptyBorder(12,12,12,12)
        preview.font = Bundle.font.deriveFont(48f)
        val inputPanel = JPanel(BorderLayout(0,12))
        inputPanel.add(JScrollPane(editor),BorderLayout.NORTH)
        inputPanel.add(JScrollPane(preview),BorderLayout.CENTER)
        val copy = JButton("入力したNRSをコピー")
        copy.addActionListener {
            try {
                Toolkit.getDefaultToolkit().systemClipboard.setContents(StringSelection(editor.text),null)
                status.text = "NRSをコピーしました。文字列は変更していません。"
            } catch (error: Exception) { status.text = "コピーできませんでした。入力欄から選択してコピーしてください。" }
        }
        inputPanel.add(copy,BorderLayout.SOUTH); tabs.addTab("入力と表示",inputPanel)
        val examples = JList(Bundle.examples.map { it.title }.toTypedArray()).apply { selectionMode = ListSelectionModel.SINGLE_SELECTION }
        val exampleText = JTextArea().readOnly().apply { font = Bundle.font.deriveFont(38f) }
        val translation = JTextArea().readOnly()
        examples.addListSelectionListener {
            val example = Bundle.examples.getOrNull(examples.selectedIndex)
            if (example != null) {
                exampleText.text = example.nrs
                translation.text = "${example.translation}\n\n${example.nrs}\n\n審査メモ\n${example.note}"
                translation.caretPosition = 0
            }
        }
        val reading = JSplitPane(JSplitPane.VERTICAL_SPLIT,JScrollPane(exampleText),JScrollPane(translation)).apply { resizeWeight = .45 }
        val examplePanel = JSplitPane(JSplitPane.VERTICAL_SPLIT,JScrollPane(examples),reading).apply { resizeWeight = .3 }
        tabs.addTab("公式例文 ${Bundle.examples.size}件",examplePanel)
        val split = JSplitPane(JSplitPane.HORIZONTAL_SPLIT,left,tabs).apply { resizeWeight = .46; dividerLocation = 470; border = null }
        left.minimumSize = Dimension(300,300); tabs.minimumSize = Dimension(400,300)
        add(split,BorderLayout.CENTER);add(status,BorderLayout.SOUTH)
        onChange(query) { filter() }; categories.addActionListener { filter() }
        onChange(editor) {
            preview.text = editor.text
            preview.caretPosition = 0
            val printable = editor.text.filterNot { it == '\n' || it == '\r' || it == '\t' }
            status.text = if (Bundle.font.canDisplayUpTo(printable) >= 0) "専用字体にない文字を含みます。入力はそのまま保持しています。" else "NRSを専用字体で表示しています。入力は終了後には保存されません。"
        }
        table.selectionModel.addListSelectionListener {
            val entry = model.rows.getOrNull(table.selectedRow)
            if (entry != null) {
                wordPreview.text = entry.nrs
                details.text = "${entry.nrs}   ${entry.ipa}\n${entry.pos}  ·  ID ${entry.id}\n\n${entry.meaningJa}\n${entry.meaningEn}\n\n${entry.notes}\n\n${entry.category}"
                details.caretPosition = 0
            }
        }
        preview.text = editor.text; filter(); table.setRowSelectionInterval(0,0); examples.selectedIndex = 0
    }
    private fun filter() {
        val category = if (categories.selectedIndex == 0) null else categories.selectedItem as String
        model.rows = Catalog.search(Bundle.entries,query.text,category)
        count.text = "${model.rows.size} / ${Bundle.entries.size}語"
        if (model.rows.isEmpty()) { wordPreview.text = ""; details.text = "一致する語がありません。検索語やカテゴリーを変えてください。" }
        else table.setRowSelectionInterval(0,0)
    }
}

private fun layoutTree(component: Component) {
    if (component is Container) { component.doLayout(); component.components.forEach(::layoutTree) }
}

fun main(args: Array<String>) {
    UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName())
    UIManager.put("defaultFont",Font("Meiryo",Font.PLAIN,14))
    val defaults=UIManager.getDefaults()
    defaults.keys().toList().filter { defaults[it] is javax.swing.plaf.FontUIResource }.forEach {
        defaults[it]=javax.swing.plaf.FontUIResource("Meiryo",Font.PLAIN,14)
    }
    if (args.contains("--self-test")) {
        check(Bundle.entries.size == 1008 && Bundle.entries.map { it.id }.toSet().size == 1008)
        check(Bundle.examples.size == 30)
        check(Catalog.search(Bundle.entries,"kyrven").any { it.id == 37 })
        check(Catalog.search(Bundle.entries,"37 KYRVEN 星雲").single().id == 37)
        check(Catalog.search(Bundle.entries,"不存在-xyz").isEmpty())
        val entry = Bundle.entries.first()
        check(Catalog.search(Bundle.entries,entry.nrs,"not-a-category").isEmpty())
        check(Bundle.font.canDisplayUpTo(Bundle.characters) == -1)
        SwingUtilities.invokeAndWait {
            val panel = StudioPanel()
            val raw = "Falun el vyrin.\n“ka?” ' ? 日本語"
            panel.editor.text = raw; check(panel.preview.text == raw)
            panel.query.text = "星雲"; check(panel.editor.text == raw && panel.preview.text == raw)
            panel.query.text = "";panel.editor.text="Falun el vyrin.";panel.setSize(1180,820);layoutTree(panel)
            val image=BufferedImage(1180,820,BufferedImage.TYPE_INT_RGB)
            val g=image.createGraphics();panel.printAll(g);g.dispose()
            val screenshot=args.getOrNull(args.indexOf("--self-test")+1)
            if (screenshot!=null) ImageIO.write(image,"png",File(screenshot))
        }
        println("PASS: 1008 entries, 30 examples, search, category, font coverage, verbatim input and independent filtering; IME/clipboard not tested")
        return
    }
    SwingUtilities.invokeLater {
        val frame=JFrame("Nebulith Studio · ${Bundle.version}")
        frame.defaultCloseOperation=JFrame.EXIT_ON_CLOSE
        frame.contentPane=StudioPanel();frame.minimumSize=Dimension(900,650);frame.setSize(1180,820)
        frame.setLocationRelativeTo(null);frame.isVisible=true
    }
}
