package com.reiun.nebulith

import java.awt.*
import java.awt.event.*
import javax.swing.*

/** Undecorated frame with app-owned controls, drag, double-click maximize and edge resizing. */
fun configureStudioWindow(frame: JFrame, panel: StudioPanel, onClose: () -> Unit) {
    frame.isUndecorated=true
    frame.defaultCloseOperation=WindowConstants.DO_NOTHING_ON_CLOSE
    frame.addWindowListener(object: WindowAdapter() { override fun windowClosing(e: WindowEvent) { onClose() } })
    fun maximize() {
        val bounds=frame.graphicsConfiguration.bounds
        val insets=Toolkit.getDefaultToolkit().getScreenInsets(frame.graphicsConfiguration)
        frame.maximizedBounds=Rectangle(bounds.x+insets.left,bounds.y+insets.top,
            bounds.width-insets.left-insets.right,bounds.height-insets.top-insets.bottom)
        frame.extendedState=if(frame.extendedState and Frame.MAXIMIZED_BOTH != 0) Frame.NORMAL else Frame.MAXIMIZED_BOTH
    }
    val controls=JPanel(FlowLayout(FlowLayout.RIGHT,2,0)).apply { isOpaque=false }
    for((label,name,action) in listOf(
        Triple("−","最小化",{ frame.extendedState=frame.extendedState or Frame.ICONIFIED }),
        Triple("□","最大化・元に戻す",{ maximize() }),
        Triple("×","閉じる",{ frame.dispatchEvent(WindowEvent(frame,WindowEvent.WINDOW_CLOSING)) }))) {
        controls.add(StudioButton(label).apply {
            font=M3Theme.font(18f); preferredSize=Dimension(36,32)
            border=BorderFactory.createEmptyBorder(4,4,4,4)
            background=M3Theme.cardBg; foreground=M3Theme.onSurfaceVariant
            toolTipText=name; accessibleContext.accessibleName=name
            addActionListener { action() }
        })
    }
    panel.windowControls.add(controls)
    var origin: Point?=null
    var position: Point?=null
    val drag=object: MouseAdapter() {
        override fun mousePressed(e: MouseEvent) { if(SwingUtilities.isLeftMouseButton(e)) { origin=e.locationOnScreen; position=frame.location } }
        override fun mouseDragged(e: MouseEvent) {
            if(frame.extendedState and Frame.MAXIMIZED_BOTH != 0) return
            val p=origin ?: return; val base=position ?: return
            frame.location=Point(base.x+e.xOnScreen-p.x,base.y+e.yOnScreen-p.y)
        }
        override fun mouseClicked(e: MouseEvent) { if(SwingUtilities.isLeftMouseButton(e) && e.clickCount==2) maximize() }
    }
    fun attach(c: Component) {
        // Only static header text/background drags; controls retain their normal input behavior.
        if(c is AbstractButton || c is JComboBox<*>) return
        c.addMouseListener(drag); c.addMouseMotionListener(drag)
        if(c is Container) c.components.forEach(::attach)
    }
    attach(panel.dragArea)
    val glass=object: JComponent() {
        override fun contains(x: Int,y: Int): Boolean = frame.extendedState and Frame.MAXIMIZED_BOTH==0 &&
            (x<6 || y<6 || x>=width-6 || y>=height-6)
    }
    var bounds: Rectangle?=null; var start: Point?=null; var edge=0
    fun edgeAt(e: MouseEvent): Int = (if(e.x<6) 1 else 0) or (if(e.x>=glass.width-6) 2 else 0) or
        (if(e.y<6) 4 else 0) or (if(e.y>=glass.height-6) 8 else 0)
    val resize=object: MouseAdapter() {
        override fun mouseMoved(e: MouseEvent) {
            val cursor=when(edgeAt(e)) { 1->Cursor.W_RESIZE_CURSOR;2->Cursor.E_RESIZE_CURSOR;4->Cursor.N_RESIZE_CURSOR;8->Cursor.S_RESIZE_CURSOR
                5->Cursor.NW_RESIZE_CURSOR;6->Cursor.NE_RESIZE_CURSOR;9->Cursor.SW_RESIZE_CURSOR;10->Cursor.SE_RESIZE_CURSOR;else->Cursor.DEFAULT_CURSOR }
            glass.cursor=Cursor.getPredefinedCursor(cursor)
        }
        override fun mousePressed(e: MouseEvent) { bounds=frame.bounds; start=e.locationOnScreen; edge=edgeAt(e) }
        override fun mouseDragged(e: MouseEvent) {
            val b=bounds ?: return; val p=start ?: return
            val dx=e.xOnScreen-p.x; val dy=e.yOnScreen-p.y
            var x=b.x; var y=b.y; var w=b.width; var h=b.height
            if(edge and 1 != 0) { w=(b.width-dx).coerceAtLeast(frame.minimumSize.width); x=b.x+b.width-w }
            if(edge and 2 != 0) w=(b.width+dx).coerceAtLeast(frame.minimumSize.width)
            if(edge and 4 != 0) { h=(b.height-dy).coerceAtLeast(frame.minimumSize.height); y=b.y+b.height-h }
            if(edge and 8 != 0) h=(b.height+dy).coerceAtLeast(frame.minimumSize.height)
            frame.setBounds(x,y,w,h)
        }
    }
    glass.addMouseListener(resize);glass.addMouseMotionListener(resize)
    frame.glassPane=glass; glass.isVisible=true
    frame.rootPane.registerKeyboardAction({frame.dispatchEvent(WindowEvent(frame,WindowEvent.WINDOW_CLOSING))},
        KeyStroke.getKeyStroke("alt F4"),JComponent.WHEN_IN_FOCUSED_WINDOW)
}
