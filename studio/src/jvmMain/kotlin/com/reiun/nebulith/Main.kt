package com.reiun.nebulith

import java.awt.*
import java.awt.datatransfer.StringSelection
import java.awt.event.MouseAdapter
import java.awt.event.MouseEvent
import java.awt.geom.Path2D
import java.awt.geom.RoundRectangle2D
import java.awt.image.BufferedImage
import java.io.File
import java.util.Base64
import javax.imageio.ImageIO
import javax.swing.*
import javax.swing.border.AbstractBorder
import javax.swing.event.DocumentEvent
import javax.swing.event.DocumentListener
import javax.swing.table.DefaultTableCellRenderer
import javax.swing.table.AbstractTableModel

object M3Theme {
    val primary = Color(0x1B, 0x5E, 0xA0)
    val onPrimary = Color(0xFF, 0xFF, 0xFF)
    val primaryContainer = Color(0xD8, 0xE4, 0xFF)
    val onPrimaryContainer = Color(0x00, 0x1D, 0x36)
    val secondary = Color(0x53, 0x5F, 0x70)
    val secondaryContainer = Color(0xD7, 0xE3, 0xF8)
    val onSecondaryContainer = Color(0x10, 0x1C, 0x2B)
    val surface = Color(0xF8, 0xF9, 0xFF)
    val surfaceVariant = Color(0xDF, 0xE2, 0xEC)
    val onSurface = Color(0x19, 0x1C, 0x20)
    val onSurfaceVariant = Color(0x43, 0x47, 0x4E)
    val outline = Color(0x73, 0x77, 0x7F)
    val outlineVariant = Color(0xC3, 0xC6, 0xD0)
    val cardBg = Color(0xFF, 0xFF, 0xFF)
    val cardSelected = Color(0xEE, 0xF4, 0xFF)
    val gold = Color(0xC5, 0x9B, 0x27)
    val chipBg = Color(0xEB, 0xEE, 0xF5)
    val fontBase: Font = Font("Segoe UI", Font.PLAIN, 14)
    val fontTitle: Font = Font("Segoe UI", Font.BOLD, 18)
    val fontSub: Font = Font("Segoe UI", Font.BOLD, 12)
}

object MaterialIcons {
    fun createIcon(type: String, size: Int = 18, color: Color = M3Theme.onSurfaceVariant): Icon = object : Icon {
        override fun getIconWidth() = size
        override fun getIconHeight() = size
        override fun paintIcon(c: Component?, g: Graphics?, x: Int, y: Int) {
            val g2 = (g as Graphics2D).create() as Graphics2D
            g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
            g2.setRenderingHint(RenderingHints.KEY_STROKE_CONTROL, RenderingHints.VALUE_STROKE_PURE)
            g2.color = color
            g2.translate(x, y)
            val s = size.toFloat()
            val scale = s / 24f
            g2.scale(scale.toDouble(), scale.toDouble())
            when (type) {
                "search" -> {
                    g2.stroke = BasicStroke(2.2f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND)
                    g2.drawOval(4, 4, 11, 11)
                    g2.drawLine(13, 13, 19, 19)
                }
                "clear" -> {
                    g2.stroke = BasicStroke(2.2f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND)
                    g2.drawLine(6, 6, 18, 18)
                    g2.drawLine(18, 6, 6, 18)
                }
                "copy" -> {
                    g2.stroke = BasicStroke(1.8f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND)
                    g2.drawRoundRect(8, 4, 11, 13, 3, 3)
                    val p = Path2D.Float()
                    p.moveTo(15f, 19f)
                    p.lineTo(5f, 19f)
                    p.curveTo(4.4f, 19f, 4f, 18.6f, 4f, 18f)
                    p.lineTo(4f, 8f)
                    g2.draw(p)
                }
                "add" -> {
                    g2.stroke = BasicStroke(2.2f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND)
                    g2.drawLine(12, 5, 12, 19)
                    g2.drawLine(5, 12, 19, 12)
                }
                "tune" -> {
                    g2.stroke = BasicStroke(2.0f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND)
                    g2.drawLine(3, 7, 21, 7)
                    g2.drawLine(3, 17, 21, 17)
                    g2.fillRect(8, 5, 4, 4)
                    g2.fillRect(14, 15, 4, 4)
                }
                "star" -> {
                    val p = Path2D.Float()
                    p.moveTo(12f, 3f); p.lineTo(14.5f, 9f); p.lineTo(21f, 9.5f)
                    p.lineTo(16f, 14f); p.lineTo(17.5f, 20.5f); p.lineTo(12f, 17f)
                    p.lineTo(6.5f, 20.5f); p.lineTo(8f, 14f); p.lineTo(3f, 9.5f)
                    p.lineTo(9.5f, 9f); p.closePath()
                    g2.fill(p)
                }
                "book" -> {
                    g2.stroke = BasicStroke(1.8f, BasicStroke.CAP_ROUND, BasicStroke.JOIN_ROUND)
                    val p1 = Path2D.Float()
                    p1.moveTo(12f, 7f); p1.curveTo(10f, 5f, 6f, 5f, 4f, 6f); p1.lineTo(4f, 19f)
                    p1.curveTo(6f, 18f, 10f, 18f, 12f, 20f); p1.closePath()
                    val p2 = Path2D.Float()
                    p2.moveTo(12f, 7f); p2.curveTo(14f, 5f, 18f, 5f, 20f, 6f); p2.lineTo(20f, 19f)
                    p2.curveTo(18f, 18f, 14f, 18f, 12f, 20f); p2.closePath()
                    g2.draw(p1); g2.draw(p2)
                }
                "category" -> {
                    g2.fillRoundRect(4, 4, 6, 6, 2, 2)
                    g2.fillRoundRect(14, 4, 6, 6, 2, 2)
                    g2.fillRoundRect(4, 14, 6, 6, 2, 2)
                    g2.fillRoundRect(14, 14, 6, 6, 2, 2)
                }
            }
            g2.dispose()
        }
    }
}

class RoundedCardBorder(val radius: Int = 16, val color: Color = M3Theme.outlineVariant) : AbstractBorder() {
    override fun paintBorder(c: Component, g: Graphics, x: Int, y: Int, width: Int, height: Int) {
        val g2 = g.create() as Graphics2D
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
        g2.color = color
        g2.draw(RoundRectangle2D.Float(x + 0.5f, y + 0.5f, width - 1f, height - 1f, radius.toFloat(), radius.toFloat()))
        g2.dispose()
    }
    override fun getBorderInsets(c: Component) = Insets(radius / 2, radius / 2, radius / 2, radius / 2)
}

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
    override fun getColumnName(column: Int) = listOf("NRS (語根)", "日本語意味", "品詞")[column]
    override fun getValueAt(row: Int, column: Int): Any = when(column) {
        0 -> rows[row].nrs; 1 -> rows[row].meaningJa; else -> rows[row].pos
    }
}

fun JTextArea.readOnly() = apply {
    isEditable = false; lineWrap = true; wrapStyleWord = true
    background = M3Theme.cardBg
    foreground = M3Theme.onSurface
    border = BorderFactory.createEmptyBorder(8, 8, 8, 8)
}

fun onChange(component: javax.swing.text.JTextComponent, action: () -> Unit) {
    component.document.addDocumentListener(object : DocumentListener {
        override fun insertUpdate(e: DocumentEvent) = action()
        override fun removeUpdate(e: DocumentEvent) = action()
        override fun changedUpdate(e: DocumentEvent) = action()
    })
}

class MaterialChip(val text: String, var isSelected: Boolean = false, val onClick: () -> Unit) : JPanel(FlowLayout(FlowLayout.CENTER, 8, 4)) {
    val label = JLabel(text)
    init {
        isOpaque = false
        cursor = Cursor.getPredefinedCursor(Cursor.HAND_CURSOR)
        label.font = M3Theme.fontSub
        add(label)
        updateAppearance()
        addMouseListener(object : MouseAdapter() {
            override fun mouseClicked(e: MouseEvent) {
                isSelected = !isSelected
                updateAppearance()
                onClick()
            }
        })
    }
    fun updateAppearance() {
        if (isSelected) {
            label.foreground = M3Theme.onPrimaryContainer
        } else {
            label.foreground = M3Theme.onSurfaceVariant
        }
        repaint()
    }
    override fun paintComponent(g: Graphics) {
        val g2 = g.create() as Graphics2D
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
        val arc = height
        if (isSelected) {
            g2.color = M3Theme.secondaryContainer
            g2.fillRoundRect(1, 1, width - 2, height - 2, arc, arc)
            g2.color = M3Theme.primary
            g2.stroke = BasicStroke(1.2f)
            g2.drawRoundRect(1, 1, width - 2, height - 2, arc, arc)
        } else {
            g2.color = M3Theme.cardBg
            g2.fillRoundRect(1, 1, width - 2, height - 2, arc, arc)
            g2.color = M3Theme.outlineVariant
            g2.stroke = BasicStroke(1f)
            g2.drawRoundRect(1, 1, width - 2, height - 2, arc, arc)
        }
        g2.dispose()
        super.paintComponent(g)
    }
}

class StudioPanel : JPanel(BorderLayout(16, 16)) {
    val query = JTextField()
    val editor = JTextArea("Falun el vyrin.", 3, 30)
    val preview = JTextArea().readOnly()
    val model = WordsModel()
    private val table = JTable(model)
    private val details = JTextArea().readOnly()
    private val wordPreview = JLabel("", SwingConstants.CENTER)
    private val count = JLabel()
    private val categories = JComboBox((listOf("全カテゴリー") + Bundle.entries.map { it.category }.distinct()).toTypedArray())
    private val status = JLabel("入力はこの画面内だけに保持します。終了後には保存されません。")
    private var selectedPos: String? = "すべて"
    private val posChipsPanel = JPanel(FlowLayout(FlowLayout.LEFT, 4, 0))
    private val relatedPanel = JPanel(FlowLayout(FlowLayout.LEFT, 4, 2))

    init {
        border = BorderFactory.createEmptyBorder(16, 16, 16, 16)
        background = M3Theme.surface

        // 1. ヘッダーバー (Material You Top App Bar)
        val header = JPanel(BorderLayout(12, 0)).apply {
            isOpaque = true
            background = M3Theme.cardBg
            border = BorderFactory.createCompoundBorder(
                RoundedCardBorder(16, M3Theme.outlineVariant),
                BorderFactory.createEmptyBorder(12, 16, 12, 16)
            )
        }
        val titleBox = JPanel(FlowLayout(FlowLayout.LEFT, 10, 0)).apply { isOpaque = false }
        val logoIcon = JLabel(MaterialIcons.createIcon("star", 26, M3Theme.gold))
        val titleText = JLabel("NEBULITH STUDIO").apply {
            font = Font("Segoe UI", Font.BOLD, 20)
            foreground = M3Theme.primary
        }
        val subText = JLabel("星石語 (Nebulith) 統合言語スタジオ").apply {
            font = M3Theme.fontBase
            foreground = M3Theme.onSurfaceVariant
        }
        titleBox.add(logoIcon); titleBox.add(titleText); titleBox.add(subText)
        header.add(titleBox, BorderLayout.WEST)

        val metaBox = JPanel(FlowLayout(FlowLayout.RIGHT, 8, 0)).apply { isOpaque = false }
        val badgeVer = JLabel(" Lexicon v23.5 ").apply {
            font = M3Theme.fontSub
            foreground = M3Theme.primary
            isOpaque = true
            background = M3Theme.primaryContainer
            border = BorderFactory.createEmptyBorder(3, 8, 3, 8)
        }
        val badgeFont = JLabel(" Font v2.5 ").apply {
            font = M3Theme.fontSub
            foreground = M3Theme.onSecondaryContainer
            isOpaque = true
            background = M3Theme.secondaryContainer
            border = BorderFactory.createEmptyBorder(3, 8, 3, 8)
        }
        val badgeTotal = JLabel(" 1,008語 (完全一括照合) ").apply {
            font = M3Theme.fontSub
            foreground = M3Theme.onSurfaceVariant
            isOpaque = true
            background = M3Theme.chipBg
            border = BorderFactory.createEmptyBorder(3, 8, 3, 8)
        }
        metaBox.add(badgeVer); metaBox.add(badgeFont); metaBox.add(badgeTotal)
        header.add(metaBox, BorderLayout.EAST)
        add(header, BorderLayout.NORTH)

        // 2. 左側：M3 検索・カテゴリ・テーブル
        val searchCard = JPanel(BorderLayout(8, 8)).apply {
            isOpaque = true
            background = M3Theme.cardBg
            border = BorderFactory.createCompoundBorder(
                RoundedCardBorder(16, M3Theme.outlineVariant),
                BorderFactory.createEmptyBorder(12, 12, 12, 12)
            )
        }
        
        // M3 検索バー
        val searchBar = JPanel(BorderLayout(8, 0)).apply {
            isOpaque = true
            background = M3Theme.surfaceVariant
            border = BorderFactory.createEmptyBorder(6, 12, 6, 12)
        }
        val searchIcon = JLabel(MaterialIcons.createIcon("search", 20, M3Theme.onSurfaceVariant))
        query.apply {
            font = Font("Segoe UI", Font.PLAIN, 15)
            background = M3Theme.surfaceVariant
            foreground = M3Theme.onSurface
            border = null
            toolTipText = "語根、意味、IPA、IDを入力して絞り込み（スペースでAND検索）"
        }
        val clearBtn = JButton(MaterialIcons.createIcon("clear", 16, M3Theme.outline)).apply {
            isContentAreaFilled = false
            isBorderPainted = false
            cursor = Cursor.getPredefinedCursor(Cursor.HAND_CURSOR)
            addActionListener { query.text = "" }
        }
        searchBar.add(searchIcon, BorderLayout.WEST)
        searchBar.add(query, BorderLayout.CENTER)
        searchBar.add(clearBtn, BorderLayout.EAST)

        // 品詞クイックチップ
        posChipsPanel.apply { isOpaque = false }
        val posList = listOf("すべて", "名", "動", "形", "副")
        val chips = mutableListOf<MaterialChip>()
        for (p in posList) {
            val chip = MaterialChip(p, isSelected = (p == "すべて")) {
                chips.forEach { c -> 
                    c.isSelected = (c.text == p)
                    c.updateAppearance() 
                }
                selectedPos = p
                filter()
            }
            chips.add(chip)
            posChipsPanel.add(chip)
        }

        // カテゴリコンボと件数
        val catBox = JPanel(BorderLayout(6, 0)).apply { isOpaque = false }
        categories.apply {
            font = M3Theme.fontBase
            background = M3Theme.cardBg
        }
        count.apply {
            font = M3Theme.fontSub
            foreground = M3Theme.primary
            horizontalAlignment = SwingConstants.RIGHT
        }
        catBox.add(categories, BorderLayout.CENTER)
        catBox.add(count, BorderLayout.EAST)

        val searchControls = JPanel(GridLayout(0, 1, 0, 8)).apply {
            isOpaque = false
            add(searchBar)
            add(posChipsPanel)
            add(catBox)
        }
        searchCard.add(searchControls, BorderLayout.CENTER)

        // テーブル (M3 スタイル)
        table.apply {
            rowHeight = 36
            setSelectionMode(ListSelectionModel.SINGLE_SELECTION)
            fillsViewportHeight = true
            font = Font("Segoe UI", Font.PLAIN, 14)
            tableHeader.font = M3Theme.fontSub
            tableHeader.background = M3Theme.chipBg
            tableHeader.foreground = M3Theme.onSurfaceVariant
            gridColor = M3Theme.surfaceVariant
            setShowHorizontalLines(true)
            setShowVerticalLines(false)
            setSelectionBackground(M3Theme.primaryContainer)
            setSelectionForeground(M3Theme.onPrimaryContainer)
            columnModel.getColumn(0).preferredWidth = 110
            columnModel.getColumn(1).preferredWidth = 260
            columnModel.getColumn(2).preferredWidth = 55
        }
        val tableScroll = JScrollPane(table).apply {
            border = BorderFactory.createCompoundBorder(
                RoundedCardBorder(16, M3Theme.outlineVariant),
                BorderFactory.createEmptyBorder(4, 4, 4, 4)
            )
            viewport.background = M3Theme.cardBg
        }

        val left = JPanel(BorderLayout(0, 10)).apply {
            isOpaque = false
            add(searchCard, BorderLayout.NORTH)
            add(tableScroll, BorderLayout.CENTER)
        }

        // 3. 右側：タブパネル (Details / Editor / Corpus / Extended)
        val tabs = JTabbedPane().apply {
            font = M3Theme.fontBase
            background = M3Theme.surface
        }

        // --- タブ1: 語の詳細 (Word Details Card) ---
        val wordDetailCard = JPanel(BorderLayout(0, 12)).apply {
            isOpaque = true
            background = M3Theme.cardBg
            border = BorderFactory.createCompoundBorder(
                RoundedCardBorder(16, M3Theme.outlineVariant),
                BorderFactory.createEmptyBorder(16, 16, 16, 16)
            )
        }

        // 大判字形表示 (Hero Glyph Card)
        val heroGlyphPanel = JPanel(BorderLayout()).apply {
            preferredSize = Dimension(400, 110)
            isOpaque = true
            background = M3Theme.primaryContainer
            border = BorderFactory.createCompoundBorder(
                RoundedCardBorder(14, M3Theme.outlineVariant),
                BorderFactory.createEmptyBorder(8, 8, 8, 8)
            )
        }
        wordPreview.apply {
            font = Bundle.font.deriveFont(58f)
            foreground = M3Theme.primary
        }
        heroGlyphPanel.add(wordPreview, BorderLayout.CENTER)

        // 詳細テキストエリア
        details.apply {
            font = Font("Segoe UI", Font.PLAIN, 15)
            lineWrap = true
            wrapStyleWord = true
        }
        val detailsScroll = JScrollPane(details).apply {
            border = BorderFactory.createCompoundBorder(
                RoundedCardBorder(12, M3Theme.outlineVariant),
                BorderFactory.createEmptyBorder(6, 6, 6, 6)
            )
            viewport.background = M3Theme.cardBg
        }

        // 関連語・派生語パネル
        relatedPanel.apply {
            isOpaque = true
            background = M3Theme.chipBg
            border = BorderFactory.createCompoundBorder(
                RoundedCardBorder(12, M3Theme.outlineVariant),
                BorderFactory.createEmptyBorder(4, 8, 4, 8)
            )
        }

        // アクションボタン群
        val btnBar = JPanel(FlowLayout(FlowLayout.RIGHT, 8, 0)).apply { isOpaque = false }
        val copyEntryBtn = JButton("引用形式をコピー", MaterialIcons.createIcon("copy", 16, M3Theme.primary)).apply {
            font = M3Theme.fontSub
            isFocusPainted = false
            background = M3Theme.secondaryContainer
            foreground = M3Theme.onSecondaryContainer
            cursor = Cursor.getPredefinedCursor(Cursor.HAND_CURSOR)
            addActionListener {
                val selected = this@StudioPanel.model.rows.getOrNull(table.selectedRow)
                if (selected != null) {
                    val text = "ID ${selected.id} ${selected.nrs} ${selected.ipa} (${selected.pos}) ${selected.meaningJa} / ${selected.meaningEn} [${selected.notes}]"
                    Toolkit.getDefaultToolkit().systemClipboard.setContents(StringSelection(text), null)
                    status.text = "辞書エントリをクリップボードにコピーしました。"
                }
            }
        }
        val insert = JButton("選択した語をエディタへ追加", MaterialIcons.createIcon("add", 16, M3Theme.onPrimary)).apply {
            font = M3Theme.fontSub
            isFocusPainted = false
            background = M3Theme.primary
            foreground = M3Theme.onPrimary
            cursor = Cursor.getPredefinedCursor(Cursor.HAND_CURSOR)
            addActionListener {
                val selected = this@StudioPanel.model.rows.getOrNull(table.selectedRow)
                if (selected != null) {
                    editor.replaceSelection(selected.nrs)
                    tabs.selectedIndex = 1
                }
            }
        }
        btnBar.add(copyEntryBtn)
        btnBar.add(insert)

        val centerInfo = JPanel(BorderLayout(0, 8)).apply {
            isOpaque = false
            add(detailsScroll, BorderLayout.CENTER)
            val relatedBox = JPanel(BorderLayout(4, 2)).apply {
                isOpaque = false
                add(JLabel("派生・関連語 (クリックでジャンプ):").apply { font = M3Theme.fontSub; foreground = M3Theme.onSurfaceVariant }, BorderLayout.NORTH)
                add(relatedPanel, BorderLayout.CENTER)
            }
            add(relatedBox, BorderLayout.SOUTH)
        }

        wordDetailCard.add(heroGlyphPanel, BorderLayout.NORTH)
        wordDetailCard.add(centerInfo, BorderLayout.CENTER)
        wordDetailCard.add(btnBar, BorderLayout.SOUTH)
        tabs.addTab("語の詳細", wordDetailCard)

        // --- タブ2: 筆記エディタ (Editor & Realtime Preview) ---
        val inputCard = JPanel(BorderLayout(0, 12)).apply {
            isOpaque = true
            background = M3Theme.cardBg
            border = BorderFactory.createCompoundBorder(
                RoundedCardBorder(16, M3Theme.outlineVariant),
                BorderFactory.createEmptyBorder(16, 16, 16, 16)
            )
        }
        editor.apply {
            font = Font("Consolas", Font.PLAIN, 18)
            lineWrap = true
            wrapStyleWord = true
            border = BorderFactory.createEmptyBorder(10, 10, 10, 10)
        }
        val editorScroll = JScrollPane(editor).apply {
            border = BorderFactory.createCompoundBorder(
                RoundedCardBorder(12, M3Theme.outlineVariant),
                BorderFactory.createEmptyBorder(4, 4, 4, 4)
            )
            preferredSize = Dimension(400, 140)
        }
        preview.apply {
            font = Bundle.font.deriveFont(46f)
            foreground = M3Theme.primary
            border = BorderFactory.createEmptyBorder(12, 12, 12, 12)
        }
        val previewScroll = JScrollPane(preview).apply {
            border = BorderFactory.createCompoundBorder(
                RoundedCardBorder(12, M3Theme.primary),
                BorderFactory.createEmptyBorder(4, 4, 4, 4)
            )
        }
        val copy = JButton("入力したNRSをコピー", MaterialIcons.createIcon("copy", 16, M3Theme.onPrimary)).apply {
            font = M3Theme.fontSub
            background = M3Theme.primary
            foreground = M3Theme.onPrimary
            isFocusPainted = false
            cursor = Cursor.getPredefinedCursor(Cursor.HAND_CURSOR)
            addActionListener {
                try {
                    Toolkit.getDefaultToolkit().systemClipboard.setContents(StringSelection(editor.text), null)
                    status.text = "NRS文字列をクリップボードにコピーしました。"
                } catch (error: Exception) {
                    status.text = "コピーできませんでした。入力欄から選択してコピーしてください。"
                }
            }
        }
        val editorTop = JPanel(BorderLayout(0, 4)).apply {
            isOpaque = false
            add(JLabel("アルファベット入力 (NRS):").apply { font = M3Theme.fontSub; foreground = M3Theme.onSurfaceVariant }, BorderLayout.NORTH)
            add(editorScroll, BorderLayout.CENTER)
        }
        val previewCenter = JPanel(BorderLayout(0, 4)).apply {
            isOpaque = false
            add(JLabel("天体記号フォント リアルタイム描画 (Nebulith-Regular v2.5):").apply { font = M3Theme.fontSub; foreground = M3Theme.primary }, BorderLayout.NORTH)
            add(previewScroll, BorderLayout.CENTER)
        }
        inputCard.add(editorTop, BorderLayout.NORTH)
        inputCard.add(previewCenter, BorderLayout.CENTER)
        inputCard.add(copy, BorderLayout.SOUTH)
        tabs.addTab("筆記エディタ", inputCard)

        // --- タブ3: 規範コーパス (Canon Corpus) ---
        val examplesList = JList(Bundle.examples.map { it.title }.toTypedArray()).apply {
            selectionMode = ListSelectionModel.SINGLE_SELECTION
            font = Font("Segoe UI", Font.PLAIN, 14)
            fixedCellHeight = 32
            background = M3Theme.cardBg
        }
        val exampleText = JTextArea().readOnly().apply {
            font = Bundle.font.deriveFont(36f)
            foreground = M3Theme.primary
        }
        val translation = JTextArea().readOnly().apply {
            font = Font("Segoe UI", Font.PLAIN, 14)
        }
        examplesList.addListSelectionListener {
            val example = Bundle.examples.getOrNull(examplesList.selectedIndex)
            if (example != null) {
                exampleText.text = example.nrs
                translation.text = "【和訳】\n${example.translation}\n\n【NRS原文】\n${example.nrs}\n\n【審査メモ・文法解説】\n${example.note}"
                translation.caretPosition = 0
            }
        }
        val reading = JSplitPane(JSplitPane.VERTICAL_SPLIT, JScrollPane(exampleText), JScrollPane(translation)).apply {
            resizeWeight = .45
            border = null
        }
        val examplePanel = JSplitPane(JSplitPane.HORIZONTAL_SPLIT, JScrollPane(examplesList).apply {
            preferredSize = Dimension(220, 300)
            border = BorderFactory.createCompoundBorder(
                RoundedCardBorder(12, M3Theme.outlineVariant),
                BorderFactory.createEmptyBorder(4, 4, 4, 4)
            )
        }, reading).apply {
            resizeWeight = .28
            border = null
        }
        tabs.addTab("規範コーパス (30例)", examplePanel)

        // 全体スプリット
        val split = JSplitPane(JSplitPane.HORIZONTAL_SPLIT, left, tabs).apply {
            resizeWeight = .44
            dividerLocation = 480
            border = null
            isOpaque = false
        }
        left.minimumSize = Dimension(320, 300)
        tabs.minimumSize = Dimension(400, 300)
        add(split, BorderLayout.CENTER)

        // ステータスバー (M3 Footer)
        val statusBar = JPanel(BorderLayout()).apply {
            isOpaque = true
            background = M3Theme.cardBg
            border = BorderFactory.createCompoundBorder(
                RoundedCardBorder(12, M3Theme.outlineVariant),
                BorderFactory.createEmptyBorder(8, 12, 8, 12)
            )
        }
        status.apply {
            font = M3Theme.fontSub
            foreground = M3Theme.onSurfaceVariant
        }
        statusBar.add(status, BorderLayout.CENTER)
        add(statusBar, BorderLayout.SOUTH)

        // イベントバインド
        onChange(query) { filter() }
        categories.addActionListener { filter() }
        onChange(editor) {
            preview.text = editor.text
            preview.caretPosition = 0
            val printable = editor.text.filterNot { it == '\n' || it == '\r' || it == '\t' }
            status.text = if (Bundle.font.canDisplayUpTo(printable) >= 0)
                "専用字体にない文字を含みます。入力はそのまま保持しています。"
            else
                "NRSを専用字体で表示しています。入力はこのセッション内でのみ有効です。"
        }
        table.selectionModel.addListSelectionListener {
            val entry = this@StudioPanel.model.rows.getOrNull(table.selectedRow)
            if (entry != null) {
                wordPreview.text = entry.nrs
                details.text = "【語根】 ${entry.nrs}      【発音】 ${entry.ipa}\n【品詞】 ${entry.pos}      【ID】 ${entry.id}      【領域】 ${entry.category}\n\n【日本語意味】\n${entry.meaningJa}\n\n【英語意味】\n${entry.meaningEn}\n\n【語源・備考】\n${entry.notes}"
                details.caretPosition = 0
                updateRelatedChips(entry)
            }
        }

        preview.text = editor.text
        filter()
        table.setRowSelectionInterval(0, 0)
        examplesList.selectedIndex = 0
    }

    private fun updateRelatedChips(entry: Entry) {
        relatedPanel.removeAll()
        val related = Catalog.findRelated(Bundle.entries, entry)
        if (related.isEmpty()) {
            relatedPanel.add(JLabel("（派生語なし）").apply { font = M3Theme.fontSub; foreground = M3Theme.outline })
        } else {
            for (r in related) {
                val chip = JButton("${r.nrs} (${r.meaningJa.split("、")[0]})").apply {
                    font = M3Theme.fontSub
                    isFocusPainted = false
                    background = M3Theme.cardBg
                    foreground = M3Theme.primary
                    cursor = Cursor.getPredefinedCursor(Cursor.HAND_CURSOR)
                    addActionListener {
                        query.text = r.nrs
                    }
                }
                relatedPanel.add(chip)
            }
        }
        relatedPanel.revalidate()
        relatedPanel.repaint()
    }

    private fun filter() {
        val category = if (categories.selectedIndex == 0) null else categories.selectedItem as String
        model.rows = Catalog.search(Bundle.entries, query.text, category, selectedPos)
        count.text = "${model.rows.size} / ${Bundle.entries.size}語"
        if (model.rows.isEmpty()) {
            wordPreview.text = ""
            details.text = "一致する語がありません。検索条件を変更してください。"
            relatedPanel.removeAll()
            relatedPanel.revalidate()
        } else {
            table.setRowSelectionInterval(0, 0)
        }
    }
}

private fun layoutTree(component: Component) {
    if (component is Container) { component.doLayout(); component.components.forEach(::layoutTree) }
}

fun main(args: Array<String>) {
    try {
        UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName())
    } catch (_: Exception) {}

    UIManager.put("defaultFont", Font("Segoe UI", Font.PLAIN, 14))
    val defaults = UIManager.getDefaults()
    defaults.keys().toList().filter { defaults[it] is javax.swing.plaf.FontUIResource }.forEach {
        defaults[it] = javax.swing.plaf.FontUIResource("Segoe UI", Font.PLAIN, 14)
    }

    if (args.contains("--self-test")) {
        check(Bundle.entries.size == 1008 && Bundle.entries.map { it.id }.toSet().size == 1008)
        check(Bundle.examples.size == 30)
        check(Catalog.search(Bundle.entries, "kyrven").any { it.id == 37 })
        check(Catalog.search(Bundle.entries, "37 KYRVEN 星雲").single().id == 37)
        check(Catalog.search(Bundle.entries, "不存在-xyz").isEmpty())
        val entry = Bundle.entries.first()
        check(Catalog.search(Bundle.entries, entry.nrs, "not-a-category").isEmpty())
        check(Bundle.font.canDisplayUpTo(Bundle.characters) == -1)
        SwingUtilities.invokeAndWait {
            val panel = StudioPanel()
            val raw = "Falun el vyrin.\n“ka?” ' ? 日本語"
            panel.editor.text = raw; check(panel.preview.text == raw)
            panel.query.text = "星雲"; check(panel.editor.text == raw && panel.preview.text == raw)
            panel.query.text = ""; panel.editor.text = "Falun el vyrin."; panel.setSize(1180, 820); layoutTree(panel)
            val image = BufferedImage(1180, 820, BufferedImage.TYPE_INT_RGB)
            val g = image.createGraphics(); panel.printAll(g); g.dispose()
            val screenshot = args.getOrNull(args.indexOf("--self-test") + 1)
            if (screenshot != null) ImageIO.write(image, "png", File(screenshot))
        }
        return
    }

    SwingUtilities.invokeLater {
        val frame = JFrame("Nebulith Studio — 星石語 統合言語スタジオ (Material You)")
        frame.defaultCloseOperation = WindowConstants.EXIT_ON_CLOSE
        frame.contentPane = StudioPanel()
        frame.setSize(1200, 840)
        frame.minimumSize = Dimension(900, 600)
        frame.setLocationRelativeTo(null)
        frame.isVisible = true
    }
}
