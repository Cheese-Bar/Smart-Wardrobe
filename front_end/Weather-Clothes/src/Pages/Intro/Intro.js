import React from "react"
import "./intro.css"

const Intro = () => {
    return(
        <section class="slides"> 
  
            <section class="slides-nav">
                <nav class="slides-nav__nav">
                <button class="slides-nav__prev js-prev">Prev</button>
                <button class="slides-nav__next js-next">Next</button>
                </nav>
            </section>

            <section class="slide is-active">
                <div class="slide__content">
                <figure class="slide__figure"><div class="slide__img" style="background-image: url(https://source.unsplash.com/nfTA8pdaq9A/2000x1100)"></div></figure>
                <header class="slide__header">
                    <h2 class="slide__title">
                    <span class="title-line"><span>Click, Key</span></span>
                    <span class="title-line"><span>Or Scroll Fool</span></span>
                    </h2>
                </header>
                </div>
            </section>

            <section class="slide">
                <div class="slide__content">
                <figure class="slide__figure"><div class="slide__img" style="background-image: url(https://source.unsplash.com/okmtVMuBzkQ/2000x1100)"></div></figure>
                <header class="slide__header">
                    <h2 class="slide__title">
                    <span class="title-line"><span>Slide Two</span></span>
                    <span class="title-line"><span>Dood Mood</span></span>
                    </h2>
                </header>
                </div>
            </section>

            <section class="slide">
                <div class="slide__content">
                <figure class="slide__figure"><div class="slide__img" style="background-image: url(https://source.unsplash.com/WuQME0I_oZA/2000x1100)"></div></figure>
                <header class="slide__header">
                    <h2 class="slide__title">
                    <span class="title-line"><span>This Right</span></span>
                    <span class="title-line"><span>Here Makes Three</span></span>
                    </h2>
                </header>
                </div>
            </section>

            <section class="slide">
                <div class="slide__content">
                <figure class="slide__figure"><div class="slide__img" style="background-image: url(https://source.unsplash.com/NsWcRlBT_74/2000x1100)"></div></figure>
                <header class="slide__header">
                    <h2 class="slide__title">
                    <span class="title-line"><span>How Now</span></span>
                    <span class="title-line"><span>Part Four More</span></span>
                    </h2>
                </header>
                </div>
            </section>
        </section>
    )
}