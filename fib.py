from manimlib.imports import *
import colorutils as cu

class Box(VGroup):
    def __init__(self, num=1, **kwargs):
        super().__init__(**kwargs)
        self.num = num
        self.L = num * 0.5
        self.create_body()

    def create_body(self):
        body = Square(side_length=self.L).set_color(BLACK)
        text = Integer(self.num).rescale_to_fit(body.get_width() / 4, dim=1)
        text.move_to(body.get_center())
        text.set_opacity(0.8)
        text.set_color(BLACK)
        self.box = VGroup(body, text)
        self.add(self.box)


class GoldenSpiral(ZoomedScene):
    CONFIG = {
        "camera_config" : {
            "background_color" : "#f1faee"
        }
    }
    def construct(self):
        a = 1
        b = 1
        s1 = Box(a)
        s2 = Box(b).shift(s1.get_width()/2 * UR)
        s1.shift(s1.get_width()/2 * (UR + RIGHT * 2)) 
        shape = VGroup(s1, s2)
        
        spiral = VGroup(
            ArcBetweenPoints(s1.get_corner(UR), s1.get_corner(DL), angle=-PI/2),
            ArcBetweenPoints(s2.get_corner(DR), s2.get_corner(UL), angle=-PI/2)
            )
        current_pt = s2.get_corner(UL)
        self.camera_frame.set_width(shape.get_width() * 2)
        # self.camera_frame.add_updater(lambda m: m.set_height(max(shape.get_height(), shape.get_width())))
        # self.add(self.camera_frame)
        self.add(s1, s2)
        directions = [UP, RIGHT, DOWN, LEFT]
        for i in range(20):
            a, b = b, a+b
            next_shape = Box(b).next_to(shape, directions[i % 4], buff=0)
            shape.add(next_shape)
            if i%2 == 0:
                self.play(
                    ApplyMethod(self.camera_frame.set_height, shape.get_height() * 2)
                )
            # else:
            #     self.play(
            #         ApplyMethod(self.camera_frame.set_width, shape.get_width() * 2)
            #     )
            self.play(DrawBorderThenFill(next_shape), run_time=0.2)
            next_arc = ArcBetweenPoints(current_pt, next_shape.get_corner(directions[i % 4] + directions[(i + 1) % 4]), angle=-PI/2)
            current_pt = next_shape.get_corner(directions[i % 4] + directions[(i + 1) % 4])
            spiral.add(next_arc)
        spiral.set_stroke(color="#e63946" , width=4.0)
        self.play(
            ShowCreation(spiral), run_time=3.0
        )
        self.wait()

class FibPetal(Scene):
    def construct(self):
        petal = VGroup()
        for n in range(2500):
            phi = n * 137.5 * TAU / 360
            r = 0.15 * np.sqrt(n)
            d = Dot()
            d.shift(np.array([r * np.cos(phi), r * np.sin(phi), 0]))
            c = cu.Color(hsv=(n % 256, 1, 1))
            d.set_color(c.hex)
            petal.add(d)

        self.play(
            AnimationGroup(
               *[GrowFromCenter(d) for d in petal], lag_ratio=0.1, run_time=6.0
            )
        )
        self.wait()

class EndScene(Scene):
    CONFIG = {
        "camera_config" : {
            "background_color" : "#f1faee"
        }
    }
    def construct(self):
        a = 1
        b = 1
        aa = Integer(a).scale(3)
        bb = Integer(b).scale(3).next_to(aa, RIGHT, buff=MED_LARGE_BUFF)
        plus = TextMobject(" + ").scale(3)
        series = VGroup(aa, bb).move_to(ORIGIN).set_color(BLACK)
        self.add(
            series
        )
        for _ in range(4):
            a, b = b, a + b
            next_n = Integer(b).scale(3).next_to(series, RIGHT, buff=MED_LARGE_BUFF).set_color(BLACK)
            x = series[-2].copy().set_color("#e63946")
            y = series[-1].copy().set_color("#e63946")
            p = plus.copy().set_color("#e63946")
            x.next_to(series, RIGHT, buff=MED_LARGE_BUFF)
            p.next_to(x, RIGHT)
            y.next_to(p, RIGHT)
            to_delete = VGroup(x, p, y)

            self.play(
                ReplacementTransform(VGroup(series[-2].copy(), series[-1].copy()), to_delete), run_time=0.8
            )
            self.play(
                ReplacementTransform(to_delete, next_n), run_time=0.2
            )
            series.add(next_n)
            self.play(
                ApplyMethod(series.move_to, ORIGIN), run_time=0.2
            )
        dots = TexMobject("\\cdots").scale(3).next_to(series, RIGHT, buff=MED_LARGE_BUFF).set_color(BLACK)
        self.play(
            Write(dots)
        )
        date = TextMobject("11", "-", "23").scale(3).set_color(BLACK).move_to(UP)
        text = TextMobject("Fibonacci Day!!").scale(3).set_color(BLACK).move_to(DOWN)
        to_delete = series[:4]
        self.play(
            ReplacementTransform(to_delete, date),
            FadeOut(series[4:]),
            FadeOut(dots)
        )
        

        self.play(Write(text))
        
        self.wait()