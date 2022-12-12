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
          r'\texttt{[}',
          r'\texttt{battery~}',
          r'\texttt{payload}',
          r'\texttt{]}'
        )
        float1[0].set_color(frgd_white)
        float1[1].set_color(frgd_white)
        float1[2].set_color(frgd_white)
        float1[3].set_color(frgd_white)
        float1.move_to([0,2,0])

        gdot1 = [0,0,0]
        gdot2 = [-2,-1,0]
        gdot3 = [+2,-1,0]
        gline12 = Line(gdot1, gdot2).set_color(frgd_purple)
        gline13 = Line(gdot1, gdot3).set_color(frgd_purple)
        gtext1 = Tex(r'\texttt{.}').move_to([0,.25,0])
        gtext2 = Tex(r'\texttt{battery}').move_to([-2,-1.25,0])
        gtext3 = Tex(r'\texttt{payload}').move_to([+2,-1.25,0])
        graph1 = VGroup(gline12, gline13,
                        gtext1, gtext2, gtext3,
                       )

        float2 = Tex(
          r'\texttt{[}',
          r'\texttt{battery~}',
          r'\texttt{[}',
          r'\texttt{sample~}',
          r'\texttt{context}',
          r'\texttt{]}',
          r'\texttt{]}'
        )
        float2[0].set_color(bkgd_dark)
        float2[1].set_color(bkgd_dark)
        float2[2].set_color(frgd_white)
        float2[3].set_color(frgd_white)
        float2[4].set_color(frgd_white)
        float2[5].set_color(frgd_white)
        float2[6].set_color(bkgd_dark)
        float2.move_to([0,2,0])

        gdot3_= [+2,-1.5,0]
        gdot6 = [+0,-2.5,0]
        gdot7 = [+4,-2.5,0]
        gline36 = Line(gdot3_, gdot6).set_color(frgd_green)
        gline37 = Line(gdot3_, gdot7).set_color(frgd_green)
        gtext6 = Tex(r'\texttt{sample}').move_to([+0,-2.75,0])
        gtext7 = Tex(r'\texttt{context}').move_to([+4,-2.75,0])
        graph2 = VGroup(gline36, gline37,
                        gtext6, gtext7,
                       )

        float3 = float2.copy()
        float3[:].set_color(frgd_white)
        float3.move_to([0,2,0])

        self.play(Write(float1), FadeIn(graph1))
        self.wait()
        self.play(TransformMatchingTex(float1, float2,
                                       transform_mismatches=True),
                  FadeIn(graph2))
        self.wait()
        self.play(TransformMatchingTex(float2, float3,
                                       transform_mismatches=True))
