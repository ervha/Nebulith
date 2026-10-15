package com.reiun.nebulith

import java.awt.*
import java.nio.file.Files
import java.nio.file.Path
import javax.imageio.ImageIO
import javax.swing.*

/** Uses an actual Windows frame, isolated from normal user state. */
fun runWindowSmokeTest(output: Path) {
    Files.createDirectories(output)
    var frame: JFrame?=null
    var panel: StudioPanel?=null
    var store: StudioStorage?=null
    fun edt(action: () -> Unit) = SwingUtilities.invokeAndWait(action)
    fun click(name: String) {
        fun find(c: Component): AbstractButton? {
            if(c is AbstractButton && c.accessibleContext.accessibleName==name) return c
            return if(c is Container) c.components.mapNotNull(::find).firstOrNull() else null
        }
        checkNotNull(find(panel!!.windowControls)).doClick()
    }
    try {
        edt {
            store=StudioStorage(output.resolve("state"))
            store!!.save(StudioState(dark=true,divider=.55))
            val f=JFrame("Nebulith Studio — Packaging test"); frame=f
            val p=StudioPanel(store); panel=p
            configureStudioWindow(f,p) { check(p.saveNow()); f.dispose() }
            f.contentPane=p; f.minimumSize=Dimension(900,600); f.setSize(1180,820); f.setLocationRelativeTo(null); f.isVisible=true
            check(f.isUndecorated)
        }
        Thread.sleep(450)
        edt {
            val p=panel!!; val f=frame!!
            check(kotlin.math.abs(p.mainSplit.dividerLocation.toDouble()/p.mainSplit.width-.55)<.02)
            p.editor.text="保存テスト\nFalun el vyrin."
            p.previewSize.value=50
            p.mainSplit.dividerLocation=(p.mainSplit.width*.45).toInt()
            val location=p.mainSplit.dividerLocation
            p.setDarkMode(false); check(p.mainSplit.dividerLocation==location)
            p.setDarkMode(true); check(p.mainSplit.dividerLocation==location)
            p.favoriteButton.doClick()
            check(p.saveNow())
            f.validate()
            val image=java.awt.image.BufferedImage(f.width,f.height,java.awt.image.BufferedImage.TYPE_INT_RGB)
            val g=image.createGraphics()
            g.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING,RenderingHints.VALUE_TEXT_ANTIALIAS_ON)
            f.paint(g); g.dispose(); ImageIO.write(image,"png",output.resolve("frameless-window.png").toFile())
            p.workspaceSelector.selectedIndex=1
            p.translator.source.text="私は赤い星を観測します。"
            p.translator.translateNow()
            check(p.translator.target.text=="Vyrel el mi ia vyr pyrin.")
            fun captureTranslation(name: String) {
                f.validate()
                val shot=java.awt.image.BufferedImage(f.width,f.height,java.awt.image.BufferedImage.TYPE_INT_RGB)
                val graphics=shot.createGraphics()
                graphics.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING,RenderingHints.VALUE_TEXT_ANTIALIAS_ON)
                f.paint(graphics);graphics.dispose();ImageIO.write(shot,"png",output.resolve(name).toFile())
            }
            p.setDarkMode(false)
            check(p.translator.target.text=="Vyrel el mi ia vyr pyrin.")
            captureTranslation("translation-light.png")
            p.setDarkMode(true);captureTranslation("translation-dark.png")
            f.setSize(900,600);captureTranslation("translation-compact.png")
            f.setSize(1180,820)
            check(p.saveNow())
            click("最大化・元に戻す")
        }
        Thread.sleep(350)
        edt { check(frame!!.extendedState and Frame.MAXIMIZED_BOTH != 0); click("最大化・元に戻す") }
        Thread.sleep(250)
        edt { check(frame!!.extendedState and Frame.MAXIMIZED_BOTH == 0); click("最小化") }
        Thread.sleep(250)
        edt { check(frame!!.extendedState and Frame.ICONIFIED != 0); frame!!.extendedState=Frame.NORMAL }
        Thread.sleep(250)
        edt { click("閉じる"); check(!frame!!.isDisplayable) }
        check(store!!.load().draft=="保存テスト\nFalun el vyrin.")
        check(store!!.load().dark && store!!.load().previewSize==50)
        check(store!!.load().translationSource=="私は赤い星を観測します。")
        Files.write(output.resolve("window-test.txt"),"PASS: real undecorated frame, restored divider, maximize/restore/minimize/close controls and saved draft/settings".toByteArray())
        println("PASS: native frameless window and controls")
    } finally {
        edt { frame?.dispose(); panel?.saveNow() }
        store?.close()
    }
}
