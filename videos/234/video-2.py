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
        
        float1 = Tex(
          r'\texttt{0}',
          r'\texttt{011.1110.1}',
          r'\texttt{000.0000.0000.0000.0000.0000}'
        )
        float1[0].set_color(frgd_white)
        float1[1].set_color(frgd_green)
        float1[2].set_color(frgd_white)

        text1 = Tex(
          r'(-1)',
          r'^{0}'
        )
        text1[0].set_color(frgd_white)
        text1[1].set_color(frgd_green)

        float2 = Tex(
          r'\texttt{0}',
          r'\texttt{011.1110.1}',
          r'\texttt{000.0000.0000.0000.0000.0000}'
        )
        float2[0].set_color(frgd_white)
        float2[1].set_color(frgd_purple)
        float2[2].set_color(frgd_white)

        text2 = Tex(
          r'2',
          r'^{125}',
          r'-127 = 2 ^ { -2 }'
        )
        text2[0].set_color(frgd_white)
        text2[1].set_color(frgd_purple)
        text2[2].set_color(frgd_white)
        
        float3 = Tex(
          r'\texttt{0}',
          r'\texttt{011.1110.1}',
          r'\texttt{000.0000.0000.0000.0000.0000}'
        )
        float3[0].set_color(frgd_white)
        float3[1].set_color(frgd_white)
        float3[2].set_color(bkgd_dark)

        text3 = Tex(
          r'[1] + ',
          r'0'
        )
        text3[0].set_color(frgd_white)
        text3[1].set_color(bkgd_dark)

        lines = VGroup(float1, text1,
                       float2, text2,
                       float3, text3)
        lines.arrange(DOWN, buff=MED_LARGE_BUFF)
        for line in lines:
          print(line)

        self.play(Write(lines[0:2]))
        #self.wait()
        self.play(Write(lines[2:4]))
        #self.wait()
        self.play(Write(lines[4:6]))
        self.wait(3)
        self.play(FadeOut(lines[0:6]))
        self.wait()
