# JJK
An interactive web-based visualizer that uses AI hand-tracking and 3D particles to recreate Cursed Techniques and Domain Expansions from Jujutsu Kaisen right in your browser.

## Description
An interactive, browser-based visualizer inspired by the anime series *Jujutsu Kaisen*. It utilizes computer vision via **MediaPipe** for real-time hand tracking, and **Three.js** to render 3D volume-based particle effects. Perform the correct hand signs on camera to manifest iconic Cursed Techniques and Domain Expansions. 

![Demo GIF](https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExa2R2aTh0d2E2cXE1Z3N6Ym9lZzY0bnpkdjB4bXBhZnJuY2s2NzNzYSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/AtdO4rsHIGeMTDGft5/giphy.gif))


## Features & Techniques

Hold the corresponding hand gesture for 1.5 seconds to charge and activate the technique:

* **Secret Technique: Hollow Purple** 🟣
    * **Visuals:** A chaotic singularity combining attraction and repulsion.
    * **Trigger:** "Pinch" gesture (Thumb + Index touching).
* **Cursed Technique Reversal: Red** 🔴
    * **Visuals:** A blinding white-hot core generating a violent sphere of repulsive force.
    * **Trigger:** Index finger pointing up.
* **Domain Expansion: Infinite Void** 🌌
    * **Visuals:** A multi-layered celestial domain featuring an event horizon and infinite cosmos.
    * **Trigger:** Index + Middle fingers pointing up.
* **Domain Expansion: Malevolent Shrine** ⛩️
    * **Visuals:** A dark, ominous red aura representing the King of Curses.
    * **Trigger:** Flat Hand (All fingers pointing up / Prayer gesture).
* **Domain Expansion: Chimera Shadow Garden** 🐺
    * **Visuals:** A floor of dark, bubbling, shadowy liquid with rising toxic shikigami spikes, crowned by the massive, glowing golden Wheel of Mahoraga hovering above.
    * **Trigger:** "Horns" gesture (Index + Pinky fingers up).
* **Domain Expansion: Coffin of the Iron Mountain** 🌋
    * **Visuals:** A massive 3D volcanic cone with a bubbling magma crater and a violent eruption of glowing embers and ash.
    * **Trigger:** Fist (All fingers folded down).

## Getting Started

### Prerequisites
You need a modern web browser (Chrome, Edge, Firefox) and an active webcam.

### Installation & Running
1.  **Clone the repo**
    ```bash
    git clone [https://github.com/HaliMauMau-PH/JJK.git](https://github.com/HaliMauMau-PH/JJK.git)
    cd JJK
    ```

2.  **Run the project**
    * **VS Code:** Install the "Live Server" extension, right-click `index.html`, and select "Open with Live Server".
    * Alternatively, you can just open the `index.html` file directly in your browser, though running it via a local server is recommended for camera permissions.
