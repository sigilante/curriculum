from manimlib import *

bkgd_dark = '#211c29'
bkgd_lite = '#ffffff'

frgd_white = '#ffffff'
frgd_purple= '#baabd1'
frgd_green = '#b7cb5f'

highlight = "#aa0000"
background = "#121214"

class MyScene(Scene):
    def construct(self):
        self.camera.background_color = bkgd_dark
        
        text1 = Tex(
          r'\frac{1}{4} = \frac{25}{100}'
        )
        text1[0].set_color(frgd_white)

        text2 = Tex(
          r'0.25'
        )
        text2[0].set_color(frgd_white)

        text3 = Tex(
          r'25 \times 10^{-2} \textrm{ or } 25\textrm{e-2}'
        )
        text3[0].set_color(frgd_white)

        text4 = Tex(
          r'(-1)',
          r'^{0}',
          r'\times',
          r'25',
          r'\times',
          r'10',
          r'^{-2}'
        )
        text4[0].set_color(frgd_white)
        text4[1].set_color(frgd_purple)
        text4[2].set_color(frgd_white)
        text4[3].set_color(frgd_green)
        text4[4].set_color(frgd_white)
        text4[5].set_color(frgd_white)
        text4[6].set_color(bkgd_dark)

        text5 = Tex(
          r'\texttt{0}',
          r'\texttt{.}',
          r'\texttt{-2}',
          r'\texttt{.}',
          r'\texttt{25}'
        )
        text5[0].set_color(frgd_purple)
        text5[1].set_color(frgd_white)
        text5[2].set_color(bkgd_dark)
        text5[3].set_color(frgd_white)
        text5[4].set_color(frgd_green)

        lines = VGroup(text1, text2, text3, text4, text5)
        lines.arrange(DOWN, buff=MED_LARGE_BUFF)

        self.play(Write(lines[0]))
        self.wait()
        self.play(Write(lines[1]))
        self.wait()
        self.play(Write(lines[2]))
        self.wait()
        self.play(Write(lines[3]))
        self.wait()
        self.play(Write(lines[4]))
        self.wait()
        self.play(FadeOut(lines))
