import express from 'express';

import { HTMX_KNOWLEDGE } from './data/htmx-info.js';

const app = express();

app.use(express.urlencoded({extended: false}));
app.use(express.static('public'));

app.get('/', (req, res) => {
  res.send(`
    <!DOCTYPE html>
    <html>
      <head>
        <title>HTMX Essentials</title>
        <link
          href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap"
          rel="stylesheet"
          
        />
        <link rel="icon" href="/icon.png" />
        <link rel="stylesheet" href="/main.css" />
        <script src="/htmx.js" defer></script>
      </head>
      <body>
        <header id="main-header">
          <img src="/htmx-logo.jpg" alt="HTMX Logo" />
          <h1>Essentials</h1>
        </header>

        <main>
          <p>HTMX is a JavaScript library that you use without writing JavaScript code.</p>

          <!-- We swap the button below with the value returned by GETing /info -->
          <!-- <button hx-get="/info" hx-swap="outerHTML">Learn More</button> -->

          <!-- We add to the target (in this case everything in <main>) with the value returned by GETing /info -->
          <!-- Multiple button clicks add the info multiple times -->
          <!-- Can trigger either mousing over with CTRL pressed, or clicking -->
          <!-- <button hx-get="/info" hx-target="main" hx-swap="beforeend" hx-trigger="mouseenter[ctrlKey],click">Learn More</button> -->

          <!-- Below does as above but fixes the multi-click issue -->
          <!-- <button hx-get="/info" hx-target="main" hx-swap="beforeend" hx-trigger="click once">Learn More</button> -->

          <!-- We can use hx-select to grab a specific part of the response, such as when we return
          with a res.redirect("/"), however we're then sending lots of data over the wire -->
          <form hx-post="/note" hx-target="ul" hx-swap="outerHTML">
            <p>
              <label for="note">Your note</label>
              <input type="text" id="note" name="note">
            </p>
            <p>
              <button>Save Note</button
            </p>
          </form>

          <ul>
            ${HTMX_KNOWLEDGE.map(info => `<li>${info}</li>`).join('')}
          </ul>
        </main>
      </body>
    </html>
  `);
});

/*
app.get('/info', (req, res) => {
  res.send(`
    <ul>
      ${HTMX_KNOWLEDGE.map(info => `<li>${info}</li>`).join('')}
    </ul>
  `);
});
*/

app.post("/note", (req, res) => {
  const note = req.body.note;
  HTMX_KNOWLEDGE.unshift(note);
  res.send(`
          <ul>
            ${HTMX_KNOWLEDGE.map(info => `<li>${info}</li>`).join('')}
          </ul>
  `);
});

app.listen(3000);
