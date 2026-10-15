package com.reiun.nebulith

import java.awt.*
import java.awt.datatransfer.StringSelection
import javax.swing.*

class TranslationPanel(initialSource: String="",initialNrs: Boolean=false,private val changed: () -> Unit = {}): JPanel(BorderLayout(0,12)) {
    val source=JTextArea(initialSource,8,30)
    val target=JTextArea().readOnly()
    val direction=JComboBox(arrayOf("日本語 → Nebulith","Nebulith → 日本語"))
    val swap=StudioButton("⇄ 入れ替え")
    val copy=StudioButton("訳文をコピー")
    val useGlyphs=JCheckBox("専用字体で表示")
    val status=JTextArea().readOnly()
    private val engine=OfflineTranslator(Bundle.entries,Bundle.examples,Bundle.translationFrames)
    private val sourceTitle=JLabel()
    private val targetTitle=JLabel()
    private val count=JLabel()
    private var revision=0
    private var worker: SwingWorker<TranslationResult,Unit>?=null
    private val timer=Timer(350) { beginTranslation() }.apply { isRepeats=false }
    var result=TranslationResult("","入力待ち")
        private set
    private var resultSource=""
    private var resultDirection=0

    init {
        background=M3Theme.cardBg
        border=BorderFactory.createCompoundBorder(RoundedCardBorder(16),BorderFactory.createEmptyBorder(12,12,12,12))
        val controls=JPanel(FlowLayout(FlowLayout.LEFT,8,0)).apply { isOpaque=false }
        direction.selectedIndex=if(initialNrs)1 else 0
        direction.font=M3Theme.fontBase; direction.accessibleContext.accessibleName="翻訳方向"
        swap.font=M3Theme.fontSub;swap.background=M3Theme.chipBg;swap.foreground=M3Theme.primary
        swap.toolTipText="成功した訳文を原文へ移して、翻訳方向を切り替えます"
        val help=StudioButton("対応文型").apply {
            font=M3Theme.fontSub;background=M3Theme.chipBg;foreground=M3Theme.onSurfaceVariant
            addActionListener {
                JOptionPane.showMessageDialog(this@TranslationPanel,
                    "完全オフライン・初版の対応範囲\n\n・公式30例文：登録された対訳\n・基本動詞：輝く／光る、歩く、食べる、観測する\n・AはBである（名詞・形容詞の補語）\n・現在、過去、未来、進行、否定、疑問（一部の組み合わせのみ）\n・観測の受動、始動・反復の一部\n・場所、目的地、所有、辞書の形容詞による修飾\n\n例：私は赤い星を観測します。\n例：水は冷たいです。\n\n主語の省略、自由な複文、未知語、任意の動詞活用は未対応です。\n辞書の先頭語義を使うため、文脈・自然さ・比喩は判定しません。\n一文でも未対応なら、文章全体の訳文を確定しません。",
                    "オフライン翻訳の対応範囲",JOptionPane.INFORMATION_MESSAGE)
            }
        }
        controls.add(direction);controls.add(swap);controls.add(help)
        add(controls,BorderLayout.NORTH)
        source.apply {
            font=M3Theme.font(17f);lineWrap=true;wrapStyleWord=true
            background=M3Theme.cardBg;foreground=M3Theme.onSurface;caretColor=M3Theme.onSurface
            border=BorderFactory.createEmptyBorder(12,12,12,12)
            accessibleContext.accessibleName="翻訳する原文"
        }
        target.font=M3Theme.font(17f);target.accessibleContext.accessibleName="変換結果"
        fun section(label: JLabel,field: JTextArea): JPanel = JPanel(BorderLayout(0,8)).apply {
            isOpaque=false
            label.font=M3Theme.fontSub;label.foreground=M3Theme.onSurfaceVariant
            add(label,BorderLayout.NORTH)
            add(JScrollPane(field).apply { border=RoundedCardBorder(10);background=M3Theme.cardBg },BorderLayout.CENTER)
        }
        val columns=JPanel(GridLayout(1,2,12,0)).apply {
            isOpaque=false;add(section(sourceTitle,source));add(section(targetTitle,target))
        }
        add(columns,BorderLayout.CENTER)
        val examples=JComboBox(arrayOf("例を入力…","私は赤い星を観測します。","私はあなたの家へ歩く。","水は冷たいです。","星は輝かない。"))
        examples.font=M3Theme.font(13f);examples.accessibleContext.accessibleName="翻訳の入力例"
        examples.addActionListener {
            if(examples.selectedIndex>0) {
                val sample=examples.selectedItem as String
                if(source.text.isBlank() || JOptionPane.showConfirmDialog(this,"現在の翻訳入力を例文で置き換えますか？","例文の入力",JOptionPane.OK_CANCEL_OPTION)==JOptionPane.OK_OPTION) {
                    direction.selectedIndex=0;source.text=sample
                }
                examples.selectedIndex=0
            }
        }
        copy.apply {
            font=M3Theme.fontSub;background=M3Theme.primary;foreground=M3Theme.onPrimary;isEnabled=false
            addActionListener {
                if(!result.complete || source.text!=resultSource || direction.selectedIndex!=resultDirection)return@addActionListener
                try { Toolkit.getDefaultToolkit().systemClipboard.setContents(StringSelection(result.text),null);status.text="訳文のNRS／日本語をコピーしました。" }
                catch(_: Exception) { status.text="コピーできませんでした。訳文を選択してコピーしてください。" }
            }
        }
        useGlyphs.apply { isOpaque=false;font=M3Theme.fontSub;foreground=M3Theme.onSurfaceVariant;addActionListener { updateFont() } }
        val footer=JPanel(BorderLayout(0,6)).apply { isOpaque=false }
        val actions=JPanel(BorderLayout(8,0)).apply {
            isOpaque=false;add(examples,BorderLayout.WEST)
            add(JPanel(FlowLayout(FlowLayout.RIGHT,6,0)).apply { isOpaque=false;add(useGlyphs);add(copy) },BorderLayout.EAST)
        }
        val statusBox=JPanel(BorderLayout(6,0)).apply {
            isOpaque=false;preferredSize=Dimension(100,62)
            add(JScrollPane(status).apply { border=null;background=M3Theme.cardBg },BorderLayout.CENTER)
            add(count,BorderLayout.EAST)
        }
        status.apply { font=M3Theme.font(12f);background=M3Theme.cardBg;foreground=M3Theme.onSurfaceVariant;rows=3;border=BorderFactory.createEmptyBorder() }
        count.font=M3Theme.fontSub;count.foreground=M3Theme.onSurfaceVariant
        footer.add(actions,BorderLayout.NORTH)
        footer.add(statusBox,BorderLayout.CENTER)
        footer.add(JLabel("対応文型のみ · 文脈は未判定 · 外部への送信なし").apply { font=M3Theme.font(11f);foreground=M3Theme.onSurfaceVariant },BorderLayout.SOUTH)
        add(footer,BorderLayout.SOUTH)
        onChange(source) { invalidateTranslation();changed() }
        direction.addActionListener { invalidateTranslation();changed() }
        swap.addActionListener {
            if(result.complete && resultSource==source.text && resultDirection==direction.selectedIndex) {
                val text=result.text;direction.selectedIndex=1-direction.selectedIndex;source.text=text
            } else if(source.text.isBlank()) direction.selectedIndex=1-direction.selectedIndex
        }
        invalidateTranslation()
    }
    private fun updateFont() {
        val nrs=direction.selectedIndex==0
        useGlyphs.isEnabled=nrs
        target.font=if(nrs && useGlyphs.isSelected) Bundle.font.deriveFont(30f) else M3Theme.font(17f)
    }
    private fun invalidateTranslation() {
        revision++;worker?.cancel(true);timer.restart()
        result=TranslationResult("","更新待ち");target.text="";copy.isEnabled=false;swap.isEnabled=source.text.isBlank()
        count.text="${source.text.length} / 4000"
        val nrs=direction.selectedIndex==0
        sourceTitle.text=if(nrs)"日本語の原文" else "Nebulithの原文（NRS）"
        targetTitle.text=if(nrs)"Nebulith（NRS）" else "日本語"
        status.text=if(source.text.isBlank())"原文を入力してください。" else "変換待ち…"
        updateFont()
    }
    private fun beginTranslation() {
        val text=source.text;val mode=direction.selectedIndex;val version=revision
        worker=object: SwingWorker<TranslationResult,Unit>() {
            override fun doInBackground()=engine.translate(text,if(mode==0)TranslationDirection.JAPANESE_TO_NRS else TranslationDirection.NRS_TO_JAPANESE)
            override fun done() {
                if(isCancelled || version!=revision)return
                try { accept(get(),text,mode) }catch(_: Exception) { accept(TranslationResult("","エラー",listOf("変換できませんでした。入力を短くして再試行してください。")),text,mode) }
            }
        }.also { it.execute() }
    }
    private fun accept(value: TranslationResult,text: String,mode: Int) {
        result=value;resultSource=text;resultDirection=mode
        target.text=value.text;target.caretPosition=0;copy.isEnabled=value.complete;swap.isEnabled=value.complete || text.isBlank()
        status.text=if(value.issues.isEmpty())value.method else value.issues.joinToString("\n")
        updateFont()
    }
    /** Deterministic synchronous path for headless UI tests only. */
    fun translateNow() {
        timer.stop();revision++;worker?.cancel(true)
        accept(engine.translate(source.text,if(direction.selectedIndex==0)TranslationDirection.JAPANESE_TO_NRS else TranslationDirection.NRS_TO_JAPANESE),source.text,direction.selectedIndex)
    }
    fun dispose() { timer.stop();worker?.cancel(true) }
}
