"use client";

import { useEffect, useState } from "react";

export default function SignatureIntro() {
  const [startDrawing, setStartDrawing] = useState(false);
  const [isFading, setIsFading] = useState(false);
  const [isDone, setIsDone] = useState(false);

  useEffect(() => {
    // Start drawing after a tiny delay to ensure CSS is ready
    const drawTimer = setTimeout(() => setStartDrawing(true), 50);

    // Timeline: ~1s drawing + 0.3s hold + 0.8s fade
    const fadeTimer = setTimeout(() => {
      setIsFading(true);
      document.documentElement.classList.add("intro-done");
    }, 1350);
    const doneTimer = setTimeout(() => setIsDone(true), 2150);

    return () => {
      clearTimeout(drawTimer);
      clearTimeout(fadeTimer);
      clearTimeout(doneTimer);
    };
  }, []);

  if (isDone) return null;

  return (
    <>
      <style jsx global>{`
        .sig-overlay {
          position: fixed;
          inset: 0;
          z-index: 9999;
          background-color: #020617;
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .sig-overlay.fading {
          animation: fadeOut 0.8s ease-out forwards;
        }

        @keyframes fadeOut {
          to {
            opacity: 0;
            pointer-events: none;
          }
        }

        .sig-stroke {
          fill: none;
          stroke: white;
          stroke-width: 5;
          stroke-linecap: round;
          stroke-dasharray: 500;
          stroke-dashoffset: 500;
        }

        .sig-overlay.drawing .sig-stroke {
          animation: drawStroke 0.07s ease-out forwards;
        }

        /* O letter - strokes 1-2 */
        .sig-overlay.drawing .s1 { animation-delay: 0s; }
        .sig-overlay.drawing .s2 { animation-delay: 0.07s; }

        /* r letter - strokes 3-4 (pen lift) */
        .sig-overlay.drawing .s3 { animation-delay: 0.16s; }
        .sig-overlay.drawing .s4 { animation-delay: 0.23s; }

        /* e letter - strokes 5-6 */
        .sig-overlay.drawing .s5 { animation-delay: 0.32s; }
        .sig-overlay.drawing .s6 { animation-delay: 0.39s; }

        /* h letter - strokes 7-8 */
        .sig-overlay.drawing .s7 { animation-delay: 0.48s; }
        .sig-overlay.drawing .s8 { animation-delay: 0.55s; }

        /* o letter - stroke 9 */
        .sig-overlay.drawing .s9 { animation-delay: 0.64s; }

        /* v letter - stroke 10 */
        .sig-overlay.drawing .s10 { animation-delay: 0.73s; }

        /* s letter - stroke 11 */
        .sig-overlay.drawing .s11 { animation-delay: 0.82s; }

        /* c letter - stroke 12 */
        .sig-overlay.drawing .s12 { animation-delay: 0.89s; }

        /* h letter - stroke 13 */
        .sig-overlay.drawing .s13 { animation-delay: 0.96s; }

        /* i dot - stroke 14 */
        .sig-overlay.drawing .s14 { animation-delay: 1.03s; }

        @keyframes drawStroke {
          to {
            stroke-dashoffset: 0;
          }
        }
      `}</style>

      <div className={`sig-overlay ${startDrawing ? "drawing" : ""} ${isFading ? "fading" : ""}`}>
        <svg
          viewBox="200 80 520 120"
          style={{ width: "80vw", maxWidth: "600px", height: "auto" }}
          fill="none"
        >
          {/* O */}
          <path className="sig-stroke s1" d="M220.228 124.394C216.295 136.784 197.467 151.923 213.286 164.067C233.494 179.581 311.081 114.354 287.264 97.9612C267.04 84.0407 230.956 101.639 227.963 116.478" />
          <path className="sig-stroke s2" d="M275.112 144.263C303.698 122.796 289.382 147.552 285.867 155.813C283.982 160.244 311.078 154.469 314.689 153.41" />

          {/* r */}
          <path className="sig-stroke s3" d="M314.689 153.41C359.924 140.146 311.373 127.238 314.689 153.41Z" />
          <path className="sig-stroke s4" d="M314.689 153.41C316.788 169.975 356.198 147.569 361.872 143.865" />

          {/* e */}
          <path className="sig-stroke s5" d="M361.872 143.865C379.996 132.033 396.654 110.1 396.142 93.0151C395.587 74.4442 371.8 126.504 361.872 143.865Z" />
          <path className="sig-stroke s6" d="M361.872 143.865C358.713 149.388 356.853 155.059 354.151 160.646C353.56 161.868 357.043 156.178 366.562 150.218C393.466 133.372 380.946 180.567 408.42 157.542" />

          {/* h */}
          <path className="sig-stroke s7" d="M408.42 157.542C422.113 146.068 406.519 142.186 408.42 157.542Z" />
          <path className="sig-stroke s8" d="M408.42 157.542C409.261 164.335 419.291 164.376 427.904 164.518C446.758 164.829 436.156 128.918 413.569 144.253" />

          {/* o */}
          <path className="sig-stroke s9" d="M443.616 141.885C461.237 189.037 461.247 141.561 494.921 144.092" />

          {/* v */}
          <path className="sig-stroke s10" d="M530.069 142.59C492.635 142.764 525.754 153.079 519.876 160.419C508.831 167.863 482.829 171.175 468.519 176" />

          {/* s */}
          <path className="sig-stroke s11" d="M567.777 142.645C548.176 142.644 535.687 158.692 551.095 168.622C563.172 176.406 592.423 158.35 598.782 153.314" />

          {/* c */}
          <path className="sig-stroke s12" d="M598.782 153.314C612.006 142.84 620.551 100.564 615.577 113.834C610.591 127.137 604.922 140.225 598.782 153.314Z" />

          {/* h */}
          <path className="sig-stroke s13" d="M598.782 153.314C586.286 179.948 593.453 164.248 617.545 156.091C635.029 150.172 619.238 171.51 629.98 172.179C645.463 173.144 652.018 163.388 658.901 155.799" />

          {/* i */}
          <path className="sig-stroke s14" d="M660.543 135.24C663.427 135.24 666.987 132.79 669 131.565" />
        </svg>
      </div>
    </>
  );
}
