package com.reiun.nebulith

import java.awt.*
import javax.swing.*
import javax.swing.plaf.ColorUIResource
import javax.swing.plaf.basic.BasicButtonUI
import javax.swing.plaf.basic.BasicTabbedPaneUI
import javax.swing.plaf.basic.BasicScrollBarUI
import javax.swing.plaf.basic.BasicSplitPaneUI
import javax.swing.plaf.basic.BasicSplitPaneDivider
import javax.swing.plaf.basic.BasicSliderUI
import javax.swing.text.JTextComponent

/** Semantic colors shared by controls, custom paint, selection and focus. */
object M3Theme {
    private val light = listOf(0x285D83,0xFDFEFF,0xE2EDF5,0x163F5D,0x596978,0xEAF0F5,0x334C60,
        0xF3F5F7,0xE9EDF1,0x202B35,0x52616F,0x71808D,0xCCD5DE,0xFFFFFF,0xEDF3F8,0x967320,0xF0F3F6)
    private val night = listOf(0x9DCBF0,0x102F46,0x243E54,0xD6EAFA,0xABBBC9,0x2B3947,0xD5E3EF,
        0x141A20,0x26313C,0xE4EBF2,0xACBAC7,0x8B9BAA,0x3F4E5C,0x1D2630,0x293C4E,0xDCC181,0x25313D)
    var dark = false
        private set
    fun colors() = (if (dark) night else light).map { Color(it) }
    private fun at(i: Int) = Color((if (dark) night else light)[i])
    val primary get()=at(0); val onPrimary get()=at(1)
    val primaryContainer get()=at(2); val onPrimaryContainer get()=at(3)
    val secondary get()=at(4); val secondaryContainer get()=at(5); val onSecondaryContainer get()=at(6)
    val surface get()=at(7); val surfaceVariant get()=at(8); val onSurface get()=at(9)
    val onSurfaceVariant get()=at(10); val outline get()=at(11); val outlineVariant get()=at(12)
    val cardBg get()=at(13); val cardSelected get()=at(14); val gold get()=at(15); val chipBg get()=at(16)
    fun themed(original: Color): Color {
        val index=light.indexOf(original.rgb and 0xFFFFFF)
        return if (index>=0) at(index) else original
    }
    fun font(size: Float, bold: Boolean=false)=getAppFont(size,bold)
    val fontBase get()=font(14f); val fontTitle get()=font(18f,true); val fontSub get()=font(12f,true)

    fun install(isDark: Boolean) {
        dark=isDark
        val defaults=mapOf("Panel.background" to surface,"Viewport.background" to cardBg,
            "Label.foreground" to onSurface,"Button.background" to secondaryContainer,"Button.foreground" to onSurface,
            "ToggleButton.background" to cardBg,"ToggleButton.foreground" to onSurface,
            "TextField.background" to surfaceVariant,"TextField.foreground" to onSurface,
            "TextArea.background" to cardBg,"TextArea.foreground" to onSurface,
            "ComboBox.background" to cardBg,"ComboBox.foreground" to onSurface,
            "ComboBox.selectionBackground" to primaryContainer,"ComboBox.selectionForeground" to onPrimaryContainer,
            "List.background" to cardBg,"List.foreground" to onSurface,
            "List.selectionBackground" to primaryContainer,"List.selectionForeground" to onPrimaryContainer,
            "Table.background" to cardBg,"Table.foreground" to onSurface,
            "TableHeader.background" to chipBg,"TableHeader.foreground" to onSurfaceVariant,
            "TabbedPane.background" to surface,"TabbedPane.foreground" to onSurfaceVariant,
            "TabbedPane.selected" to cardBg,"TabbedPane.focus" to primary,
            "TabbedPane.contentAreaColor" to cardBg,"TabbedPane.borderHightlightColor" to outlineVariant,
            "ScrollBar.background" to surface,"ScrollBar.thumb" to outlineVariant,
            "ScrollBar.thumbDarkShadow" to outlineVariant,"ScrollBar.thumbHighlight" to outlineVariant,
            "ScrollPane.background" to cardBg,"SplitPane.highlight" to surface,"SplitPane.shadow" to surface,
            "SplitPane.background" to surface,"SplitPane.dividerFocusColor" to primaryContainer,
            "ToolTip.background" to cardBg,"ToolTip.foreground" to onSurface,
            "control" to surface,"controlText" to onSurface,"controlHighlight" to surfaceVariant,
            "controlShadow" to outlineVariant,"controlDkShadow" to outlineVariant)
        defaults.forEach { (key,value)->UIManager.put(key,ColorUIResource(value)) }
    }

    fun refresh(root: Component, previous: List<Color>) {
        val carets=mutableListOf<Triple<JTextComponent,Int,Int>>()
        val scrolls=mutableListOf<Pair<JViewport,Point>>()
        val dividers=mutableListOf<Pair<JSplitPane,Int>>()
        val focus=KeyboardFocusManager.getCurrentKeyboardFocusManager().focusOwner
        fun remember(c: Component) {
            if(c is JTextComponent) carets.add(Triple(c,c.caret.mark,c.caret.dot))
            if(c is JViewport) scrolls.add(c to c.viewPosition)
            if(c is JSplitPane) dividers.add(c to c.dividerLocation)
            if(c is Container) c.components.forEach(::remember)
        }
        remember(root)
        SwingUtilities.updateComponentTreeUI(root)
        fun visit(c: Component) {
            fun mapped(color: Color?): Color? {
                val index=previous.indexOf(color)
                return if(index>=0) colors()[index] else color
            }
            c.background=mapped(c.background); c.foreground=mapped(c.foreground)
            if(c is JTextComponent) {
                c.caretColor=onSurface; c.selectionColor=primaryContainer; c.selectedTextColor=onPrimaryContainer
            }
            if(c is StudioButton) c.setUI(BasicButtonUI())
            if(c is JTabbedPane) c.setUI(StudioTabsUI())
            if(c is JScrollBar) c.setUI(StudioScrollBarUI())
            if(c is JScrollPane) {
                c.background=cardBg
                if(c.border is javax.swing.plaf.UIResource) c.border=RoundedCardBorder(8,outlineVariant)
            }
            if(c is JSlider) c.setUI(StudioSliderUI(c))
            if(c is JSplitPane) {
                c.setUI(StudioSplitPaneUI())
                c.border=BorderFactory.createEmptyBorder()
                c.dividerSize=10
                (c.ui as? BasicSplitPaneUI)?.divider?.apply { border=BorderFactory.createEmptyBorder(); background=surface }
            }
            if(c is JTable) { c.selectionBackground=primaryContainer; c.selectionForeground=onPrimaryContainer; c.gridColor=surfaceVariant }
            if(c is JList<*>) { c.selectionBackground=primaryContainer; c.selectionForeground=onPrimaryContainer }
            if(c is Container) c.components.forEach(::visit)
        }
        visit(root)
        carets.forEach { (c,mark,dot)->
            c.caretPosition=mark.coerceAtMost(c.document.length)
            c.moveCaretPosition(dot.coerceAtMost(c.document.length))
        }
        scrolls.forEach { (viewport,position)->viewport.viewPosition=position }
        dividers.forEach { (split,position)->split.dividerLocation=position }
        if(focus!=null && SwingUtilities.isDescendingFrom(focus,root)) focus.requestFocusInWindow()
        root.repaint()
    }
}

class StudioSplitPaneUI: BasicSplitPaneUI() {
    override fun createDefaultDivider(): BasicSplitPaneDivider = object: BasicSplitPaneDivider(this) {
        override fun paint(g: Graphics) {
            g.color=M3Theme.surface; g.fillRect(0,0,width,height)
            g.color=M3Theme.outlineVariant
            if(orientation==JSplitPane.HORIZONTAL_SPLIT) g.fillRoundRect(width/2-1,height/2-14,2,28,2,2)
            else g.fillRoundRect(width/2-14,height/2-1,28,2,2,2)
        }
    }
}

class StudioSliderUI(slider: JSlider): BasicSliderUI(slider) {
    override fun paintTrack(g: Graphics) {
        g.color=M3Theme.outlineVariant
        g.fillRoundRect(trackRect.x,trackRect.y+trackRect.height/2-2,trackRect.width,4,4,4)
    }
    override fun paintThumb(g: Graphics) {
        val g2=g.create() as Graphics2D
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING,RenderingHints.VALUE_ANTIALIAS_ON)
        g2.color=M3Theme.primary
        g2.fillOval(thumbRect.x,thumbRect.y+3,thumbRect.width,thumbRect.width)
        g2.dispose()
    }
    override fun paintFocus(g: Graphics) {
        g.color=M3Theme.primary
        g.drawRect(focusRect.x,focusRect.y,focusRect.width-1,focusRect.height-1)
    }
}

class StudioTabsUI: BasicTabbedPaneUI() {
    override fun installDefaults() {
        super.installDefaults()
        tabInsets=Insets(10,16,10,16)
        selectedTabPadInsets=Insets(0,0,0,0)
        tabAreaInsets=Insets(0,0,0,0)
        contentBorderInsets=Insets(12,0,0,0)
    }
    override fun paintTabBackground(g: Graphics, placement: Int, index: Int, x: Int, y: Int, w: Int, h: Int, selected: Boolean) {
        g.color=if(selected) M3Theme.cardBg else M3Theme.surface
        g.fillRect(x,y,w,h)
    }
    override fun paintTabBorder(g: Graphics, placement: Int, index: Int, x: Int, y: Int, w: Int, h: Int, selected: Boolean) {
        if(selected) { g.color=M3Theme.primary; g.fillRect(x+12,y+h-3,w-24,3) }
    }
    override fun paintContentBorder(g: Graphics, placement: Int, selected: Int) {}
    override fun paintFocusIndicator(g: Graphics, placement: Int, rects: Array<Rectangle>, index: Int, iconRect: Rectangle, textRect: Rectangle, selected: Boolean) {
        if(tabPane.hasFocus() && selected) {
            val r=rects[index]; g.color=M3Theme.primary; g.drawRect(r.x+3,r.y+3,r.width-7,r.height-7)
        }
    }
}

class StudioScrollBarUI: BasicScrollBarUI() {
    private fun invisibleArrow()=JButton().apply { preferredSize=Dimension(0,0); minimumSize=Dimension(0,0); maximumSize=Dimension(0,0) }
    override fun createDecreaseButton(orientation: Int)=invisibleArrow()
    override fun createIncreaseButton(orientation: Int)=invisibleArrow()
    override fun getPreferredSize(c: JComponent)=Dimension(10,10)
    override fun paintTrack(g: Graphics,c: JComponent,r: Rectangle) { g.color=M3Theme.cardBg; g.fillRect(r.x,r.y,r.width,r.height) }
    override fun paintThumb(g: Graphics,c: JComponent,r: Rectangle) {
        if(r.isEmpty || !scrollbar.isEnabled) return
        val g2=g.create() as Graphics2D
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING,RenderingHints.VALUE_ANTIALIAS_ON)
        g2.color=M3Theme.outlineVariant; g2.fillRoundRect(r.x+2,r.y+2,(r.width-4).coerceAtLeast(3),(r.height-4).coerceAtLeast(3),8,8); g2.dispose()
    }
}

/** Flat buttons with visible keyboard focus and restrained hover treatment. */
class StudioButton(text: String="", icon: Icon?=null): JButton(text,icon) {
    constructor(icon: Icon):this("",icon)
    init {
        setUI(BasicButtonUI()); isOpaque=false; isContentAreaFilled=false; isBorderPainted=false
        border=BorderFactory.createEmptyBorder(9,14,9,14)
        cursor=Cursor.getPredefinedCursor(Cursor.HAND_CURSOR)
        isRolloverEnabled=true
    }
    override fun paintComponent(g: Graphics) {
        val g2=g.create() as Graphics2D
        g2.setRenderingHint(RenderingHints.KEY_ANTIALIASING,RenderingHints.VALUE_ANTIALIAS_ON)
        g2.color=background
        g2.fillRoundRect(1,1,width-2,height-2,12,12)
        if(model.isRollover || model.isPressed) {
            g2.color=Color(M3Theme.onSurface.red,M3Theme.onSurface.green,M3Theme.onSurface.blue,if(model.isPressed) 28 else 12)
            g2.fillRoundRect(1,1,width-2,height-2,12,12)
        }
        if(hasFocus()) {
            g2.color=M3Theme.primary; g2.stroke=BasicStroke(2f)
            g2.drawRoundRect(2,2,width-5,height-5,12,12)
        }
        g2.dispose(); super.paintComponent(g)
    }
}
