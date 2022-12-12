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

        self.play(Write(float1))
        float1_ = float1.copy()
        float1_[1].set_color(frgd_green)
        self.play(FadeTransform(float1, float1_,
                                transform_mismatches=True))
        self.wait()
        float1__ = float1.copy()
        float1__[1].set_color(frgd_white)
        float1__[2].set_color(frgd_green)
        self.play(FadeTransform(float1_, float1__,
                                transform_mismatches=True))
        self.wait()
        self.play(FadeOut(float1__))

        ####

        float2 = Text(
            '''
            ::  (a*b)+c
            |=  [a=@ b=@ c=@]
            (add (mul a b) c)
            '''
          ,font='Ubuntu Mono'
        )
        self.play(Write(float2))
        self.wait()
        float2_ = Text(
            '''
            ::  (a*b)+c
            |=  [a=@ b=@ c=@]
            (add (mul a b) c)
            '''
          ,font='Ubuntu Mono'
          ,t2c={'(add (mul a b) c)': frgd_purple}
        )
        self.play(FadeTransform(float2, float2_,
                                transform_mismatches=True))
        self.wait()
        float2__ = Text(
            '''
            ::  (a*b)+c
            |=  [a=@ b=@ c=@]
            (add (mul a b) c)
            '''
          ,font='Ubuntu Mono'
          ,t2c={'[a=@ b=@ c=@]': frgd_purple}
        )
        self.play(FadeTransform(float2_, float2__,
                                transform_mismatches=True))
        self.wait()
        self.play(FadeOut(float2__))

        ####

        float3 = Text(
            '''
            |.  code
            '''
          ,font='Ubuntu Mono'
        )
        self.play(Write(float3))
        self.wait()
        float3_ = Text(
            '''
            |.  code


            |%
            ++  $
              a
            --
            '''
          ,font='Ubuntu Mono'
          ,t2c={'code': frgd_purple}
        )
        self.play(FadeTransform(float3, float3_,
                                transform_mismatches=True))
        self.wait()
        float3__ = Text(
            '''
            |-  code


            =<  $
            |%
            ++  $
              code
            --
            '''
          ,font='Ubuntu Mono'
          ,t2c={'code': frgd_purple}
        )
        self.play(FadeTransform(float3_, float3__,
                                transform_mismatches=True))
        self.wait()
        self.play(FadeOut(float3__))

        ####

        float4 = Text(
            '''
            |=  args
            code
            '''
          ,font='Ubuntu Mono'
        )
        self.play(Write(float4))
        self.wait()
        float4_ = Text(
            '''
            |=  args
            code

            =+  args
            |%
            ++  $
              code
            --
            '''
          ,font='Ubuntu Mono'
          ,t2c={'args': frgd_purple}
        )
        self.play(FadeTransform(float4, float4_,
                                transform_mismatches=True))
        self.wait()
        float4__ = Text(
            '''
            |=  args
            code

            =+  args
            |%
            ++  $
              code
            --
            '''
          ,font='Ubuntu Mono'
          ,t2c={'code': frgd_purple}
        )
        self.play(FadeTransform(float4_, float4__,
                                transform_mismatches=True))
        self.wait()
        self.play(FadeOut(float4__))

        ####

        float5 = Text(
            '''
            |^
            code
            ++  arm-1
              code-1
            ++  arm-2
              code-2
            --
            '''
          ,font='Ubuntu Mono'
        )
        self.play(Write(float5))
        self.wait()
        float5_ = Text(
            '''
            |^
            code
            ++  arm-1
              code-1
            ++  arm-2
              code-2
            --

            =>  |%
                ++  $
                  code
                ++  arm-1
                  code-1
                ++  arm-2
                  code-2
                --
            $
            '''
          ,font='Ubuntu Mono'
        )
        self.play(FadeTransform(float5, float5_,
                                transform_mismatches=True))
        self.wait()
        self.play(FadeOut(float5_))

        ####

        float6 = Text(
            '''
            |%
            ++  arm-1
              code-1
            ++  arm-2
              code-2
            …
            ++  arm-n
              code-n
            --
            '''
          ,font='Ubuntu Mono'
        )
        self.play(Write(float6))
        self.wait()
        self.play(FadeOut(float6))

        ####

        float7 = Text(
            '''
            |_  args
            ++  arm-1
              code-1
            ++  arm-2
              code-2
            --
            '''
          ,font='Ubuntu Mono'
        )
        self.play(Write(float7))
        self.wait()
        float7_ = Text(
            '''
            |_  args
            ++  arm-1
              code-1
            ++  arm-2
              code-2
            --

            =|  a=spec
            |%
            ++  arm-1
              code-1
            ++  arm-2
              code-2
            --
            '''
          ,font='Ubuntu Mono'
        )
        self.play(FadeTransform(float7, float7_,
                                transform_mismatches=True))
        self.wait()
        self.play(FadeOut(float7_))
