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
import javax.swing.table.AbstractTableModel

private object AppFonts { val available by lazy { GraphicsEnvironment.getLocalGraphicsEnvironment().availableFontFamilyNames.toSet() } }

fun getAppFont(size: Float, bold: Boolean = false): Font {
    val candidates = listOf("Yu Gothic UI", "Meiryo", "MS UI Gothic", "Segoe UI", "Noto Sans CJK JP", "Dialog")
    val available = AppFonts.available
    val chosen = candidates.firstOrNull { it in available } ?: "Dialog"
    val style = if (bold) Font.BOLD else Font.PLAIN
    return Font(chosen, style, size.toInt())
}

object MaterialIcons {
    fun createIcon(type: String, size: Int = 18, color: Color = M3Theme.onSurfaceVariant): Icon = object : Icon {
        private val colorRole = M3Theme.colors().indexOf(color)
        override fun getIconWidth() = size
        override fun getIconHeight() = size
        override fun paintIcon(c: Component?, g: Graphics?, x: Int, y: Int) {
            val g2 = (g as Graphics2D).create() as Graphics2D
            g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
            g2.setRenderingHint(RenderingHints.KEY_STROKE_CONTROL, RenderingHints.VALUE_STROKE_PURE)
            g2.color = if (colorRole >= 0) M3Theme.colors()[colorRole] else color
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

class RoundedCardBorder(val radius: Int = 12, val color: Color = M3Theme.outlineVariant) : AbstractBorder() {
    private val colorRole = M3Theme.colors().indexOf(color)
    override fun paintBorder(c: Component, g: Graphics, x: Int, y: Int, width: Int, height: Int) {
        val g2 = g.create() as Graphics2D
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
        g2.color = if (colorRole >= 0) M3Theme.colors()[colorRole] else color
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
    val translationFrames: Map<Int,TranslationFrame> by lazy {
        lines("translation-frames.tsv").filter { it.isNotBlank() }.associate { line ->
            val c=line.split('\t')
            fun values(i: Int)=c[i].split(',').filter { it.isNotEmpty() }.toSet()
            c[0].toInt() to TranslationFrame(values(1),values(2),values(3))
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
    override fun getColumnName(column: Int) = listOf("語幹 (NRS)", "日本語意味", "品詞")[column]
    override fun getValueAt(row: Int, column: Int): Any = when(column) {
        0 -> rows[row].nrs; 1 -> rows[row].meaningJa; else -> rows[row].pos
    }
}

fun JTextArea.readOnly() = apply {
    isEditable = false; lineWrap = true; wrapStyleWord = true
    background = M3Theme.cardBg
    foreground = M3Theme.onSurface
    font = M3Theme.fontBase
    border = BorderFactory.createEmptyBorder(8, 8, 8, 8)
}

fun onChange(component: javax.swing.text.JTextComponent, action: () -> Unit) {
    component.document.addDocumentListener(object : DocumentListener {
        override fun insertUpdate(e: DocumentEvent) = action()
        override fun removeUpdate(e: DocumentEvent) = action()
        override fun changedUpdate(e: DocumentEvent) = action()
    })
}

class MaterialChip(text: String, isSelected: Boolean = false, val onClick: () -> Unit) : JToggleButton(text, isSelected) {
    init {
        font = M3Theme.fontSub
        isOpaque = false; isContentAreaFilled = false; isBorderPainted = false
        border = BorderFactory.createEmptyBorder(7, 14, 7, 14)
        cursor = Cursor.getPredefinedCursor(Cursor.HAND_CURSOR)
        addActionListener { onClick() }
        updateAppearance()
    }
    fun updateAppearance() {
        foreground = if (isSelected) M3Theme.onPrimaryContainer else M3Theme.onSurfaceVariant
        repaint()
    }
    override fun paintComponent(g: Graphics) {
        foreground = if (isSelected) M3Theme.onPrimaryContainer else M3Theme.onSurfaceVariant
        val g2 = g.create() as Graphics2D
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING, RenderingHints.VALUE_ANTIALIAS_ON)
        g2.color = if (isSelected) M3Theme.primaryContainer else M3Theme.chipBg
        g2.fillRoundRect(1, 1, width-2, height-2, 12, 12)
        if (hasFocus()) {
            g2.color = M3Theme.primary; g2.stroke = BasicStroke(2f)
            g2.drawRoundRect(2, 2, width-5, height-5, 12, 12)
        }
        g2.dispose(); super.paintComponent(g)
    }
}

class StudioPanel(private val storage: StudioStorage? = null) : JPanel(BorderLayout(16, 16)) {
    private val restored = storage?.load() ?: StudioState()
    private val favorites = restored.favorites.toMutableSet()
    private val history = restored.history.toMutableList()
    private var ready = false
    private var filtering = false
    private var dirty = false
    private val saveTimer = Timer(600) { saveNow() }.apply { isRepeats = false }
    lateinit var mainSplit: JSplitPane
        private set
    private var splitInitialized = false
    private var dividerRatio = restored.divider
    val scope = JComboBox(arrayOf("すべての語", "お気に入り", "閲覧履歴"))
    val favoriteButton = StudioButton("☆ お気に入り")
    val clearHistoryButton = StudioButton("履歴を消去")
    val windowControls = JPanel(FlowLayout(FlowLayout.RIGHT, 0, 0)).apply { isOpaque = false }
    lateinit var dragArea: JPanel
        private set
    val query = JTextField()
    val editor = JTextArea(restored.draft, 3, 30)
    val preview = JTextArea().readOnly()
    val model = WordsModel()
    val themeSelector = JComboBox(arrayOf("ライト", "ダーク"))
    val previewSize = JSlider(24, 64, restored.previewSize)
    val tabs = JTabbedPane()
    val table = JTable(model)
    val translator = TranslationPanel(restored.translationSource,restored.translationFromNrs) { queueSave() }
    val workspaceSelector = JComboBox(arrayOf("辞書・筆記", "文章の相互変換"))
    private val details = JTextArea().readOnly()
    private val wordPreview = JLabel("", SwingConstants.CENTER)
    private val count = JLabel()
    private val categories = JComboBox((listOf("全カテゴリー") + Bundle.entries.map { it.category }.distinct()).toTypedArray())
    private val status = JLabel("設定と下書きはこの端末に自動保存されます。")
    private var selectedPos: String? = "すべて"
    private val posChipsPanel = JPanel(FlowLayout(FlowLayout.LEFT, 4, 0))
    private val selectionActions = mutableListOf<AbstractButton>()
    private val relatedPanel = JPanel(FlowLayout(FlowLayout.LEFT, 4, 2))

    init {
        border = BorderFactory.createEmptyBorder(8, 8, 8, 8)
        background = M3Theme.surface

        // 1. ヘッダーバー (Material You Top App Bar)
        val header = JPanel(BorderLayout(12, 0)).apply {
            isOpaque = true
            background = M3Theme.cardBg
            border = BorderFactory.createCompoundBorder(
                RoundedCardBorder(16, M3Theme.outlineVariant),
                BorderFactory.createEmptyBorder(4, 12, 4, 12)
            )
        }
        val titleBox = JPanel(BorderLayout(12, 0)).apply { isOpaque = false }
        val logoIcon = JLabel(MaterialIcons.createIcon("star", 26, M3Theme.gold))
        val titleText = JLabel("Nebulith Studio").apply {
            font = M3Theme.font(20f, bold = true)
            foreground = M3Theme.primary
        }
        val subText = JLabel("星石語を探す、書く、読む。").apply {
            font = M3Theme.font(14f)
            foreground = M3Theme.onSurfaceVariant
        }
        titleBox.add(logoIcon, BorderLayout.WEST)
        titleBox.add(JPanel(GridLayout(2, 1, 0, 2)).apply {
            isOpaque = false; add(titleText); add(subText)
        }, BorderLayout.CENTER)
        dragArea = header
        header.add(titleBox, BorderLayout.WEST)

        val metaBox = JPanel(FlowLayout(FlowLayout.RIGHT, 8, 0)).apply { isOpaque = false }
        metaBox.add(JLabel(Bundle.version + "  ·  " + Bundle.entries.size + "語").apply {
            font = M3Theme.font(12f); foreground = M3Theme.onSurfaceVariant
        })
        themeSelector.apply {
            font = M3Theme.font(13f)
            accessibleContext.accessibleName = "表示テーマ"
            toolTipText = "ライト／ダークの切り替え（このセッション中のみ）"
            addActionListener { setDarkMode(selectedIndex == 1) }
        }
        metaBox.add(themeSelector)
        metaBox.add(windowControls)
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
            font = M3Theme.font(15f)
            background = M3Theme.surfaceVariant
            foreground = M3Theme.onSurface
            border = null
            toolTipText = "語幹・意味・IPA・IDで検索（空白でAND検索） · Ctrl+L"
            accessibleContext.accessibleName = "辞書検索"
            caretColor = M3Theme.onSurface
        }
        val clearBtn = StudioButton(MaterialIcons.createIcon("clear", 16, M3Theme.outline)).apply {
            isContentAreaFilled = false
            isBorderPainted = false
            cursor = Cursor.getPredefinedCursor(Cursor.HAND_CURSOR)
            toolTipText = "検索語を消去"
            accessibleContext.accessibleName = "検索語を消去"
            addActionListener { query.text = ""; query.requestFocusInWindow() }
        }
        searchBar.add(searchIcon, BorderLayout.WEST)
        searchBar.add(query, BorderLayout.CENTER)
        searchBar.add(clearBtn, BorderLayout.EAST)

        // 品詞クイックチップ
        posChipsPanel.apply { isOpaque = false }
        val posList = listOf("すべて", "名", "動", "形", "副", "接")
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

        val scopeBox = JPanel(BorderLayout(6, 0)).apply {
            isOpaque = false; add(scope, BorderLayout.CENTER); add(clearHistoryButton, BorderLayout.EAST)
        }
        scope.apply {
            font = M3Theme.fontBase; accessibleContext.accessibleName = "辞書の表示範囲"
            addActionListener { clearHistoryButton.isVisible = selectedIndex == 2; filter() }
        }
        clearHistoryButton.apply {
            isVisible = false; font = M3Theme.fontSub; background = M3Theme.chipBg; foreground = M3Theme.onSurfaceVariant
            addActionListener { history.clear(); queueSave(); filter() }
        }
        val searchControls = JPanel().apply {
            isOpaque = false; layout = BoxLayout(this, BoxLayout.Y_AXIS)
            listOf(searchBar to 40, posChipsPanel to 36, catBox to 34, scopeBox to 34).forEachIndexed { index, (control, height) ->
                control.alignmentX = Component.LEFT_ALIGNMENT
                control.preferredSize = Dimension(100, height)
                control.maximumSize = Dimension(Int.MAX_VALUE, height)
                if (index > 0) add(Box.createVerticalStrut(8))
                add(control)
            }
        }
        searchCard.add(searchControls, BorderLayout.CENTER)

        // テーブル (M3 スタイル)
        table.apply {
            rowHeight = 40
            background = M3Theme.cardBg
            foreground = M3Theme.onSurface
            intercellSpacing = Dimension(12, 1)
            setSelectionMode(ListSelectionModel.SINGLE_SELECTION)
            fillsViewportHeight = true
            font = M3Theme.font(14f)
            tableHeader.preferredSize = Dimension(100, 30)
            tableHeader.defaultRenderer = object : javax.swing.table.DefaultTableCellRenderer() {
                override fun getTableCellRendererComponent(t: JTable?, value: Any?, selected: Boolean, focused: Boolean, row: Int, column: Int): Component {
                    super.getTableCellRendererComponent(t, value, selected, focused, row, column)
                    background = M3Theme.chipBg; foreground = M3Theme.onSurfaceVariant
                    font = M3Theme.fontSub; border = BorderFactory.createEmptyBorder(4, 8, 4, 8)
                    return this
                }
            }
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
            setColumnHeaderView(table.tableHeader)
            border = BorderFactory.createCompoundBorder(
                RoundedCardBorder(16, M3Theme.outlineVariant),
                BorderFactory.createEmptyBorder(4, 4, 4, 4)
            )
            background = M3Theme.cardBg
            viewport.background = M3Theme.cardBg
        }

        val left = JPanel(BorderLayout(0, 10)).apply {
            isOpaque = false
            add(searchCard, BorderLayout.NORTH)
            add(tableScroll, BorderLayout.CENTER)
        }

        // 3. 右側：タブパネル (Details / Editor / Corpus)
        tabs.apply {
            font = M3Theme.font(14f, bold = true)
            background = M3Theme.surface
        }

        // --- タブ1: 語の詳細 (Word Details Card) ---
        val wordDetailCard = JPanel(BorderLayout(0, 12)).apply {
            isOpaque = true
            background = M3Theme.cardBg
            border = BorderFactory.createCompoundBorder(
                RoundedCardBorder(16, M3Theme.outlineVariant),
                BorderFactory.createEmptyBorder(8, 8, 8, 8)
            )
        }

        // 大判字形表示 (Hero Glyph Card)
        val heroGlyphPanel = JPanel(BorderLayout()).apply {
            preferredSize = Dimension(400, 90)
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
            font = M3Theme.font(15f)
            lineWrap = true
            wrapStyleWord = true
        }
        val detailsScroll = JScrollPane(details).apply {
            border = BorderFactory.createCompoundBorder(
                RoundedCardBorder(12, M3Theme.outlineVariant),
                BorderFactory.createEmptyBorder(6, 6, 6, 6)
            )
            background = M3Theme.cardBg
            viewport.background = M3Theme.cardBg
        }

        // 関連語・派生語パネル
        relatedPanel.apply {
            layout = BoxLayout(this, BoxLayout.X_AXIS)
            isOpaque = true
            background = M3Theme.chipBg
            border = BorderFactory.createCompoundBorder(
                RoundedCardBorder(12, M3Theme.outlineVariant),
                BorderFactory.createEmptyBorder(4, 8, 4, 8)
            )
        }

        // アクションボタン群
        val btnBar = JPanel(GridLayout(1, 0, 6, 0)).apply { isOpaque = false }
        val copyEntryBtn = StudioButton("語の情報をコピー", MaterialIcons.createIcon("copy", 16, M3Theme.primary)).apply {
            font = M3Theme.fontSub
            isFocusPainted = true
            background = M3Theme.secondaryContainer
            foreground = M3Theme.onSecondaryContainer
            cursor = Cursor.getPredefinedCursor(Cursor.HAND_CURSOR)
            addActionListener {
                val selected = this@StudioPanel.model.rows.getOrNull(table.selectedRow)
                if (selected != null) {
                    val text = "ID ${selected.id} ${selected.nrs} ${selected.ipa} (${selected.pos}) ${selected.meaningJa} / ${selected.meaningEn} [${selected.notes}]"
                    copyText(text, "語の情報をコピーしました。")
                }
            }
        }
        val insert = StudioButton("エディタへ追加", MaterialIcons.createIcon("add", 16, M3Theme.onPrimary)).apply {
            font = M3Theme.fontSub
            isFocusPainted = true
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
        favoriteButton.apply {
            font = M3Theme.fontSub; background = M3Theme.chipBg; foreground = M3Theme.primary
            addActionListener {
                val entry = this@StudioPanel.model.rows.getOrNull(table.selectedRow)
                if (entry != null) {
                    if (!favorites.add(entry.id)) favorites.remove(entry.id)
                    text = if (entry.id in favorites) "★ 登録済み" else "☆ お気に入り"
                    queueSave()
                    if (scope.selectedIndex == 1) filter()
                }
            }
        }
        selectionActions.addAll(listOf(copyEntryBtn, insert, favoriteButton))
        btnBar.add(favoriteButton)
        btnBar.add(copyEntryBtn)
        btnBar.add(insert)

        val centerInfo = JPanel(BorderLayout(0, 8)).apply {
            isOpaque = false
            add(detailsScroll, BorderLayout.CENTER)
            val relatedBox = JPanel(BorderLayout(4, 2)).apply {
                isOpaque = false
                add(JLabel("派生・関連語 (クリックでジャンプ):").apply { font = M3Theme.fontSub; foreground = M3Theme.onSurfaceVariant }, BorderLayout.NORTH)
                add(JScrollPane(relatedPanel, ScrollPaneConstants.VERTICAL_SCROLLBAR_NEVER, ScrollPaneConstants.HORIZONTAL_SCROLLBAR_AS_NEEDED).apply {
                    border = null; preferredSize = Dimension(100, 62); background = M3Theme.cardBg
                }, BorderLayout.CENTER)
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
                BorderFactory.createEmptyBorder(8, 8, 8, 8)
            )
        }
        editor.apply {
            font = M3Theme.font(18f)
            background = M3Theme.cardBg
            foreground = M3Theme.onSurface
            accessibleContext.accessibleName = "NRS入力"
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
            font = Bundle.font.deriveFont(previewSize.value.toFloat())
            foreground = M3Theme.primary
            border = BorderFactory.createEmptyBorder(12, 12, 12, 12)
        }
        val previewScroll = JScrollPane(preview).apply {
            border = BorderFactory.createCompoundBorder(
                RoundedCardBorder(12, M3Theme.primary),
                BorderFactory.createEmptyBorder(4, 4, 4, 4)
            )
        }
        val copy = StudioButton("入力したNRSをコピー", MaterialIcons.createIcon("copy", 16, M3Theme.onPrimary)).apply {
            font = M3Theme.fontSub
            background = M3Theme.primary
            foreground = M3Theme.onPrimary
            isFocusPainted = true
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
            add(JPanel(BorderLayout()).apply {
                isOpaque = false
                add(JLabel("専用字体プレビュー").apply { font = M3Theme.fontSub; foreground = M3Theme.onSurfaceVariant }, BorderLayout.WEST)
                val sizeLabel = JLabel("${previewSize.value} px").apply { font = M3Theme.fontSub; foreground = M3Theme.onSurfaceVariant }
                previewSize.apply {
                    preferredSize = Dimension(150, 28); isOpaque = false
                    toolTipText = "プレビュー文字サイズ"
                    accessibleContext.accessibleName = "プレビュー文字サイズ"
                    addChangeListener { preview.font = Bundle.font.deriveFont(value.toFloat()); sizeLabel.text = "${value} px"; queueSave() }
                }
                add(JPanel(BorderLayout(6, 0)).apply {
                    isOpaque = false; add(previewSize, BorderLayout.CENTER); add(sizeLabel, BorderLayout.EAST)
                }, BorderLayout.EAST)
            }, BorderLayout.NORTH)
            add(previewScroll, BorderLayout.CENTER)
        }
        inputCard.add(editorTop, BorderLayout.NORTH)
        inputCard.add(previewCenter, BorderLayout.CENTER)
        inputCard.add(copy, BorderLayout.SOUTH)
        tabs.addTab("筆記エディタ", inputCard)

        // --- タブ3: 規範コーパス (Canon Corpus) ---
        val examplesList = JList(Bundle.examples.map { it.title }.toTypedArray()).apply {
            selectionMode = ListSelectionModel.SINGLE_SELECTION
            font = M3Theme.font(14f)
            fixedCellHeight = 32
            background = M3Theme.cardBg
        }
        val exampleText = JTextArea().readOnly().apply {
            font = Bundle.font.deriveFont(36f)
            foreground = M3Theme.primary
        }
        val translation = JTextArea().readOnly().apply {
            font = M3Theme.font(14f)
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
        tabs.addTab("例文・読み物 (${Bundle.examples.size})", examplePanel)

        // 全体スプリット
        val split = JSplitPane(JSplitPane.HORIZONTAL_SPLIT, left, tabs).apply {
            resizeWeight = .38
            dividerLocation = 430
            border = null
            isOpaque = false
        }
        left.minimumSize = Dimension(320, 300)
        tabs.minimumSize = Dimension(400, 300)
        mainSplit = split
        split.addPropertyChangeListener(JSplitPane.DIVIDER_LOCATION_PROPERTY) {
            if (ready && splitInitialized && split.width > 0 && split.isShowing) {
                dividerRatio = (split.dividerLocation.toDouble() / split.width).coerceIn(.15, .85)
                queueSave()
            }
        }
        split.addComponentListener(object : java.awt.event.ComponentAdapter() {
            override fun componentResized(e: java.awt.event.ComponentEvent) {
                if (split.width > 0 && !splitInitialized) {
                    val ratio = dividerRatio
                    split.dividerLocation = (split.width * ratio).toInt()
                    dividerRatio = ratio
                    splitInitialized = true
                }
            }
        })
        val workspaces = JPanel(CardLayout()).apply {
            isOpaque = false; add(split, "dictionary"); add(translator, "translation")
        }
        workspaceSelector.apply {
            font = M3Theme.fontBase; accessibleContext.accessibleName = "作業画面"
            addActionListener { (workspaces.layout as CardLayout).show(workspaces, if(selectedIndex==0) "dictionary" else "translation") }
        }
        add(JPanel(BorderLayout(0, 10)).apply {
            isOpaque = false
            add(JPanel(BorderLayout()).apply {
                isOpaque = false; add(workspaceSelector, BorderLayout.WEST)
                add(JLabel("オフライン · 日本語 ⇄ Nebulith").apply { font = M3Theme.fontSub; foreground = M3Theme.onSurfaceVariant }, BorderLayout.EAST)
            }, BorderLayout.NORTH)
            add(workspaces, BorderLayout.CENTER)
        }, BorderLayout.CENTER)

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
                "NRSを専用字体で表示しています。下書きを自動保存します。"
        }
        table.selectionModel.addListSelectionListener { event ->
            val entry = this@StudioPanel.model.rows.getOrNull(table.selectedRow)
            if (entry != null) {
                favoriteButton.text = if (entry.id in favorites) "★ 登録済み" else "☆ お気に入り"
                if (!filtering && !event.valueIsAdjusting) recordVisit(entry.id)
                wordPreview.text = entry.nrs
                details.text = "${entry.nrs}  ${entry.ipa}\n${entry.pos}  ·  #${entry.id}  ·  ${entry.category}\n\n日本語\n${entry.meaningJa}\n\nEnglish\n${entry.meaningEn}\n\n注記\n${entry.notes}"
                details.caretPosition = 0
                updateRelatedChips(entry)
            }
        }

        table.addMouseListener(object : MouseAdapter() {
            override fun mouseClicked(e: MouseEvent) { model.rows.getOrNull(table.selectedRow)?.let { recordVisit(it.id) } }
        })
        onChange(editor) { queueSave() }
        preview.text = editor.text
        filter()
        table.setRowSelectionInterval(0, 0)
        examplesList.selectedIndex = 0
        getInputMap(WHEN_ANCESTOR_OF_FOCUSED_COMPONENT).put(KeyStroke.getKeyStroke("control L"), "search")
        actionMap.put("search", object : AbstractAction() {
            override fun actionPerformed(e: java.awt.event.ActionEvent) {
                val field = if(workspaceSelector.selectedIndex==1) translator.source else query
                field.requestFocusInWindow(); field.selectAll()
            }
        })
        query.getInputMap().put(KeyStroke.getKeyStroke("ESCAPE"), "clear-search")
        query.actionMap.put("clear-search", object : AbstractAction() {
            override fun actionPerformed(e: java.awt.event.ActionEvent) { query.text = "" }
        })
        M3Theme.refresh(this, M3Theme.colors())
        query.border = BorderFactory.createEmptyBorder(2, 0, 2, 0)
        setDarkMode(restored.dark)
        status.text = storage?.loadProblem ?: "設定と下書きはこの端末に自動保存されます。"
        ready = true
    }

    private fun recordVisit(id: Int) {
        if (!ready || history.firstOrNull() == id) return
        history.remove(id); history.add(0, id)
        while (history.size > 50) history.removeAt(history.lastIndex)
        queueSave()
    }
    private fun queueSave() {
        if (!ready || storage == null) return
        dirty = true; saveTimer.restart()
    }
    fun saveNow(): Boolean {
        saveTimer.stop()
        if (storage == null || !dirty) return true
        return try {
            storage.save(StudioState(M3Theme.dark, previewSize.value, dividerRatio, editor.text, favorites.toSet(), history.toList(), translator.source.text, translator.direction.selectedIndex == 1))
            dirty = false
            val printable = editor.text.filterNot { it == '\n' || it == '\r' || it == '\t' }
            status.text = if (Bundle.font.canDisplayUpTo(printable) >= 0)
                "保存しました。専用字体にない文字も入力のまま保持しています。" else "下書きと設定を保存しました。"
            true
        } catch (_: Exception) {
            status.text = storage.loadProblem ?: "保存できませんでした。入力をコピーして保管してください。"
            false
        }
    }

    fun setDarkMode(dark: Boolean) {
        if (dark == M3Theme.dark) return
        val previous = M3Theme.colors()
        M3Theme.install(dark)
        M3Theme.refresh(this, previous)
        query.border = BorderFactory.createEmptyBorder(2, 0, 2, 0)
        if (themeSelector.selectedIndex != if (dark) 1 else 0) themeSelector.selectedIndex = if (dark) 1 else 0
        queueSave()
    }

    private fun copyText(text: String, success: String) {
        try {
            Toolkit.getDefaultToolkit().systemClipboard.setContents(StringSelection(text), null)
            status.text = success
        } catch (_: Exception) { status.text = "コピーできませんでした。文字列を選択してコピーしてください。" }
    }

    private fun updateRelatedChips(entry: Entry) {
        relatedPanel.removeAll()
        val related = Catalog.findRelated(Bundle.entries, entry)
        if (related.isEmpty()) {
            relatedPanel.add(JLabel("（派生語なし）").apply { font = M3Theme.fontSub; foreground = M3Theme.outline })
        } else {
            for (r in related) {
                val chip = StudioButton("${r.nrs} (${r.meaningJa.split("、")[0]})").apply {
                    font = M3Theme.fontSub
                    isFocusPainted = true
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
        val selectedId = model.rows.getOrNull(table.selectedRow)?.id
        filtering = true
        val found = Catalog.search(Bundle.entries, query.text, category, selectedPos)
        model.rows = when (scope.selectedIndex) {
            1 -> found.filter { it.id in favorites }
            2 -> found.filter { it.id in history }.sortedBy { history.indexOf(it.id) }
            else -> found
        }
        count.text = "${model.rows.size} / ${Bundle.entries.size}語"
        selectionActions.forEach { it.isEnabled = model.rows.isNotEmpty() }
        if (model.rows.isEmpty()) {
            wordPreview.text = ""
            details.text = "一致する語がありません。検索条件を変更してください。"
            relatedPanel.removeAll()
            relatedPanel.revalidate()
        } else {
            val index = model.rows.indexOfFirst { it.id == selectedId }.coerceAtLeast(0)
            table.setRowSelectionInterval(index, index)
        }
        filtering = false
    }
}

private fun layoutTree(component: Component) {
    if (component is Container) { component.doLayout(); component.components.forEach(::layoutTree) }
}

fun main(args: Array<String>) {
    try {
        UIManager.setLookAndFeel(UIManager.getCrossPlatformLookAndFeelClassName())
    } catch (_: Exception) {}

    val defaultAppFont = getAppFont(14f)
    UIManager.put("defaultFont", defaultAppFont)
    val defaults = UIManager.getDefaults()
    defaults.keys().toList().filter { defaults[it] is javax.swing.plaf.FontUIResource }.forEach {
        defaults[it] = javax.swing.plaf.FontUIResource(defaultAppFont)
    }

    M3Theme.install(false)

    if (args.contains("--translation-self-test")) {
        SwingUtilities.invokeAndWait { checkOfflineTranslation() }
        return
    }
    if (args.contains("--self-test")) {
        fun luminance(c: Color): Double {
            fun linear(v: Int): Double { val s=v/255.0; return if(s<=0.04045) s/12.92 else Math.pow((s+0.055)/1.055,2.4) }
            return .2126*linear(c.red)+.7152*linear(c.green)+.0722*linear(c.blue)
        }
        for(dark in listOf(false,true)) {
            M3Theme.install(dark)
            for((fg,bg) in listOf(M3Theme.onSurface to M3Theme.cardBg, M3Theme.onSurfaceVariant to M3Theme.surface,
                    M3Theme.onPrimary to M3Theme.primary, M3Theme.onPrimaryContainer to M3Theme.primaryContainer,
                    M3Theme.onSecondaryContainer to M3Theme.secondaryContainer, M3Theme.primary to M3Theme.cardBg)) {
                val a=luminance(fg); val b=luminance(bg)
                check((maxOf(a,b)+.05)/(minOf(a,b)+.05)>=4.5) { "Insufficient text contrast" }
            }
        }
        M3Theme.install(false)
        check(Bundle.entries.size == 1008 && Bundle.entries.map { it.id }.toSet().size == 1008)
        check(Bundle.examples.size == 30)
        check(Catalog.search(Bundle.entries, "kyrven").any { it.id == 37 })
        check(Catalog.search(Bundle.entries, "37 KYRVEN 星雲").single().id == 37)
        check(Catalog.search(Bundle.entries, "不存在-xyz").isEmpty())
        val entry = Bundle.entries.first()
        check(Catalog.search(Bundle.entries, entry.nrs, "not-a-category").isEmpty())
        check(Bundle.font.canDisplayUpTo(Bundle.characters) == -1)
        SwingUtilities.invokeAndWait {
            checkOfflineTranslation()
            val panel = StudioPanel()
            val raw = "Falun el vyrin.\n“ka?” ' ? 日本語"
            panel.editor.text = raw; check(panel.preview.text == raw)
            panel.query.text = "星雲"; check(panel.editor.text == raw && panel.preview.text == raw)
            panel.editor.caretPosition = 9; panel.editor.moveCaretPosition(2)
            panel.tabs.selectedIndex = 1
            val selectedId = panel.model.rows[panel.table.selectedRow].id
            for (dark in listOf(true, false, true, false)) {
                panel.setDarkMode(dark)
                check(M3Theme.dark == dark)
                check(panel.editor.text == raw && panel.preview.text == raw)
                check(panel.editor.selectionStart == 2 && panel.editor.selectionEnd == 9)
                check(panel.editor.caret.mark == 9 && panel.editor.caret.dot == 2)
                check(panel.query.text == "星雲" && panel.tabs.selectedIndex == 1)
                check(panel.model.rows[panel.table.selectedRow].id == selectedId)
                check(panel.editor.foreground == M3Theme.onSurface)
                check(panel.editor.background == M3Theme.cardBg)
                check(panel.editor.caretColor == M3Theme.onSurface)
                check(panel.table.background == M3Theme.cardBg)
            }
            panel.previewSize.value = 56
            check(panel.preview.font.size == 56 && panel.editor.text == raw)
            panel.query.text = "不存在-xyz"; check(panel.model.rowCount == 0)
            check(panel.editor.text == raw)
            panel.query.text = ""; panel.editor.text = "Falun el vyrin."
            val screenshot = args.getOrNull(args.indexOf("--self-test") + 1)
            fun capture(path: String, width: Int, height: Int) {
                panel.setSize(width, height); layoutTree(panel)
                val image = BufferedImage(width, height, BufferedImage.TYPE_INT_RGB)
                val g = image.createGraphics()
                g.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON)
                panel.paint(g); g.dispose(); ImageIO.write(image, "png", File(path))
            }
            if(screenshot != null) {
                panel.tabs.selectedIndex = 0
                capture(screenshot, 1180, 820)
                panel.setDarkMode(true)
                capture(screenshot.replace(".png", "-dark.png"), 1180, 820)
                panel.tabs.selectedIndex = 1
                capture(screenshot.replace(".png", "-editor-dark.png"), 1000, 700)
                panel.tabs.selectedIndex = 2
                capture(screenshot.replace(".png", "-reading-dark.png"), 1180, 820)
                panel.setDarkMode(false)
                panel.tabs.selectedIndex = 0
                capture(screenshot.replace(".png", "-compact.png"), 900, 600)
            }
            val temp = java.nio.file.Files.createTempDirectory("nebulith-state-test-")
            try {
                StudioStorage(temp).use { store ->
                    store.save(StudioState(divider=.57))
                    val saved = StudioPanel(store)
                    saved.editor.text = ""
                    saved.previewSize.value = 58
                    saved.setDarkMode(true)
                    saved.translator.source.text = raw
                    saved.translator.direction.selectedIndex = 1
                    saved.favoriteButton.doClick()
                    saved.table.setRowSelectionInterval(1, 1)
                    check(saved.saveNow())
                    val state = store.load()
                    check(state.draft == "" && state.dark && state.previewSize == 58 && state.divider == .57)
                    check(state.favorites == setOf(1) && state.history == listOf(2))
                    check(state.translationSource == raw && state.translationFromNrs)
                    check(runCatching { StudioStorage(temp).close() }.isFailure)
                }
                StudioStorage(temp).use { store ->
                    val reopened = StudioPanel(store)
                    check(reopened.editor.text == "" && reopened.previewSize.value == 58 && M3Theme.dark)
                    check(reopened.translator.source.text == raw && reopened.translator.direction.selectedIndex == 1)
                    reopened.scope.selectedIndex = 1
                    check(reopened.model.rows.single().id == 1)
                    reopened.scope.selectedIndex = 2
                    check(reopened.model.rows.single().id == 2)
                    reopened.clearHistoryButton.doClick()
                    check(reopened.model.rowCount == 0)
                    reopened.editor.text = raw
                    reopened.translator.source.text = ""
                    reopened.translator.direction.selectedIndex = 0
                    check(reopened.saveNow())
                }
                StudioStorage(temp).use { store ->
                    check(store.load().draft == raw && store.load().history.isEmpty())
                    check(store.load().translationSource == "" && !store.load().translationFromNrs)
                }
                check(java.nio.file.Files.exists(temp.resolve("studio.properties.bak")))
                java.nio.file.Files.write(temp.resolve("studio.properties"), "broken-original".toByteArray())
                StudioStorage(temp).use { store ->
                    store.load(); check(store.loadProblem != null)
                    check(runCatching { store.save(StudioState()) }.isFailure)
                    check(String(java.nio.file.Files.readAllBytes(temp.resolve("studio.properties"))) == "broken-original")
                }
            } finally {
                check(temp.fileName.toString().startsWith("nebulith-state-test-"))
                check(temp.toAbsolutePath().parent == java.nio.file.Paths.get(System.getProperty("java.io.tmpdir")).toAbsolutePath().normalize())
                temp.toFile().deleteRecursively()
            }
            panel.translator.dispose()
            println("PASS: resources, search, preview, theme/selection, settings and empty/Unicode draft restart, favorites/history, lock and corrupt-state protection")
        }
        return
    }

    if (args.contains("--window-self-test")) {
        runWindowSmokeTest(java.nio.file.Paths.get(args[args.indexOf("--window-self-test") + 1]))
        return
    }
    SwingUtilities.invokeLater {
        val frame = JFrame("Nebulith Studio — 星石語")
        val storage = try { StudioStorage() } catch (e: Exception) {
            JOptionPane.showMessageDialog(null, e.message ?: "保存先を開けません。", "Nebulith Studio", JOptionPane.WARNING_MESSAGE)
            return@invokeLater
        }
        val panel = StudioPanel(storage)
        configureStudioWindow(frame, panel) {
            if (!panel.saveNow()) {
                val choice = JOptionPane.showConfirmDialog(frame, "保存できませんでした。保存せずに終了しますか？", "下書きの保存", JOptionPane.YES_NO_OPTION)
                if (choice != JOptionPane.YES_OPTION) return@configureStudioWindow
            }
            storage.close(); frame.dispose(); System.exit(0)
        }
        frame.contentPane = panel
        if (args.contains("--dark")) panel.setDarkMode(true)
        frame.setSize(1200, 840)
        frame.minimumSize = Dimension(900, 600)
        frame.setLocationRelativeTo(null)
        frame.isVisible = true
    }
}
