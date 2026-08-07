from manim import *
import numpy as np

class Scene1RootShiftTrajectory(ThreeDScene):
    def construct(self):
        # ---------------------------------------------------------
        # 1. Setup Layout and Titles (Plane expanded to fit lambda = 5+5i)
        # ---------------------------------------------------------
        left_plane = ComplexPlane(
            x_range=[-1, 6, 1],
            y_range=[-1, 6, 1],
            x_length=5,
            y_length=5,
            background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 1,
                "stroke_opacity": 0.4
            }
        ).to_edge(LEFT, buff=0.5)

        right_axes = ThreeDAxes(
            x_range=[-2, 2, 1],
            y_range=[-2, 2, 1],
            z_range=[-3, 3, 1],
            x_length=5,
            y_length=5,
            z_length=5
        ).to_edge(RIGHT, buff=0.5)

        left_title = Text("Complex Symbol Space (λ)", font_size=18, color=WHITE).next_to(left_plane, UP, buff=0.2)
        right_title = Text("3D Boundary Fiber Geometry", font_size=18, color=WHITE).next_to(right_axes, UP, buff=0.2)

        self.add_fixed_in_frame_mobjects(left_plane, left_title, right_title)

        self.play(
            Create(left_plane),
            Create(right_axes),
            Write(left_title),
            Write(right_title),
            run_time=1.5
        )

        # ---------------------------------------------------------
        # 2. Parameter Trackers & Left Panel
        # ---------------------------------------------------------
        t_tracker = ValueTracker(0.0)

        lambda_dot = always_redraw(
            lambda: Dot(
                left_plane.n2p(complex(t_tracker.get_value(), t_tracker.get_value())),
                color=YELLOW,
                radius=0.08
            )
        )

        trajectory_line = always_redraw(
            lambda: Line(
                left_plane.n2p(0),
                left_plane.n2p(complex(t_tracker.get_value(), t_tracker.get_value())),
                color=YELLOW_A,
                stroke_width=2
            )
        )

        lambda_label = always_redraw(
            lambda: MathTex(
                f"\\lambda = {t_tracker.get_value():.2f} + {t_tracker.get_value():.2f}i",
                font_size=16,
                color=YELLOW
            ).next_to(lambda_dot, UR, buff=0.05)
        )

        self.add_fixed_in_frame_mobjects(lambda_dot, lambda_label, trajectory_line)
        self.play(FadeIn(lambda_dot), Create(trajectory_line))

        # ---------------------------------------------------------
        # 3. Right Panel (Surface with Im(d) Color Gradient)
        # ---------------------------------------------------------
        def generate_fiber_surface():
            t = t_tracker.get_value()
            
            if t < 0.03:
                return Sphere(center=right_axes.c2p(1, 0, 0), radius=0.08, color=YELLOW)

            u_min, u_max = 0.15, 0.7
            v_min, v_max = 0, TAU
            u_res, v_res = 24, 36

            def surface_func(r, theta):
                b_re = 1 + r * np.cos(theta)
                b_im = r * np.sin(theta)
                b = complex(b_re, b_im)
                lam = complex(t, t)
                
                d = (1 - b) / (2 * lam * (b ** 2))
                d_re = np.clip(d.real, -3, 3)
                return right_axes.c2p(b_re, b_im, d_re)

            surface = Surface(
                surface_func,
                u_range=[u_min, u_max],
                v_range=[v_min, v_max],
                resolution=(u_res, v_res),
                stroke_width=0.2,
                fill_opacity=0.85
            )

            # Map Im(d) to TEAL -> RED gradient
            u_vals = np.linspace(u_min, u_max, u_res + 1)
            v_vals = np.linspace(v_min, v_max, v_res + 1)
            im_min, im_max = -1.5, 1.5

            face_idx = 0
            for i in range(u_res):
                u_mid = (u_vals[i] + u_vals[i + 1]) / 2
                for j in range(v_res):
                    v_mid = (v_vals[j] + v_vals[j + 1]) / 2

                    b = complex(1 + u_mid * np.cos(v_mid), u_mid * np.sin(v_mid))
                    lam = complex(t, t)
                    d = (1 - b) / (2 * lam * (b ** 2))

                    alpha = np.clip((d.imag - im_min) / (im_max - im_min), 0, 1)
                    face_color = interpolate_color(TEAL_C, RED_C, alpha)

                    if face_idx < len(surface.submobjects):
                        surface.submobjects[face_idx].set_fill(face_color, opacity=0.85)
                        surface.submobjects[face_idx].set_stroke(face_color, width=0.1)
                    face_idx += 1

            return surface

        fiber_surface = always_redraw(generate_fiber_surface)
        self.add(fiber_surface)

        # ---------------------------------------------------------
        # 4. Camera & Animation Sequence (Trajectory up to 5.0)
        # ---------------------------------------------------------
        self.move_camera(phi=70 * DEGREES, theta=-45 * DEGREES, run_time=2)

        self.play(
            t_tracker.animate.set_value(5.0),
            run_time=8,
            rate_func=linear
        )

        self.wait(1)