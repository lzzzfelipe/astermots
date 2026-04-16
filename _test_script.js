
    let dictionary = [];
    let activeIndex = -1;
    let acceptedPairs = []; // {input, word}

    // --- French phonetic normalization engine ---
    function phonetic(str) {
      let s = str.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').trim();

      // Multi-char replacements (order matters — longest first)
      const rules = [
        [/eaux/g, 'o'],
        [/eau/g, 'o'],
        [/aux/g, 'o'],
        [/au/g, 'o'],
        [/ou/g, 'u'],
        [/oi/g, 'wa'],
        [/ain/g, 'in'],
        [/ein/g, 'in'],
        [/aim/g, 'in'],
        [/eim/g, 'in'],
        [/en(?=[^aeiou]|$)/g, 'an'],
        [/em(?=[bp])/g, 'an'],
        [/an(?=[^aeiou]|$)/g, 'an'],
        [/am(?=[bp])/g, 'an'],
        [/on(?=[^aeiou]|$)/g, 'on'],
        [/om(?=[bp])/g, 'on'],
        [/un(?=[^aeiou]|$)/g, 'in'],
        [/ph/g, 'f'],
        [/qu/g, 'k'],
        [/gu(?=[ei])/g, 'g'],
        [/ch/g, 'sh'],
        [/gn/g, 'ny'],
        [/tion/g, 'sion'],
        [/th/g, 't'],
        [/rh/g, 'r'],
        [/ll/g, 'l'],
        [/ss/g, 's'],
        [/tt/g, 't'],
        [/mm/g, 'm'],
        [/nn/g, 'n'],
        [/pp/g, 'p'],
        [/ff/g, 'f'],
        [/cc/g, 'k'],
        [/rr/g, 'r'],
        [/ee/g, 'e'],
        [/oo/g, 'o'],
        [/aa/g, 'a'],
        [/ii/g, 'i'],
        // c before e/i = s
        [/c(?=[ei])/g, 's'],
        // c elsewhere = k
        [/c/g, 'k'],
        // g before e/i = j
        [/g(?=[ei])/g, 'j'],
        // Silent trailing consonants (common in French)
        [/([aeiou])[stdxzp]$/g, '$1'],
        [/e$/g, ''],
        // y as vowel
        [/y/g, 'i'],
        // w
        [/w/g, 'v'],
        // x as sh (kids often write x for the ch sound) — must be before h removal
        [/x/g, 'sh'],
        // silent h
        [/h/g, ''],
      ];

      for (const [re, rep] of rules) {
        s = s.replace(re, rep);
      }

      return s;
    }

    function searchWords(query) {
      if (!query) return [];
      const pq = phonetic(query);
      const lq = query.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');

      const scored = [];
      for (const entry of dictionary) {
        let score = 0;

        // Exact prefix on the word
        const lw = entry.word.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
        if (lw.startsWith(lq)) {
          score = 100;
        }

        // Phonetic prefix match
        if (entry._phonetic.startsWith(pq)) {
          score = Math.max(score, 80);
        }

        // Phonetic contains
        if (score === 0 && entry._phonetic.includes(pq)) {
          score = 30;
        }

        // Fuzzy phonetic (Levenshtein on short inputs)
        if (score === 0 && pq.length >= 3) {
          const dist = levenshtein(pq, entry._phonetic.slice(0, pq.length + 2));
          if (dist <= Math.max(1, Math.floor(pq.length / 3))) {
            score = 20;
          }
        }

        if (score > 0) {
          // Compute phonetic distance (absolute highest priority tiebreaker)
          const phonDist = levenshtein(pq, entry._phonetic);
          const litDist = levenshtein(lq, lw);
          scored.push({ entry, score, phonDist, litDist });
        }
      }

      // Sort: match tier → phonetic distance → frequency → literal similarity
      scored.sort((a, b) => {
        if (b.score !== a.score) return b.score - a.score;
        if (a.phonDist !== b.phonDist) return a.phonDist - b.phonDist;
        const freqDiff = (a.entry.freq || 99999) - (b.entry.freq || 99999);
        if (freqDiff !== 0) return freqDiff;
        return a.litDist - b.litDist;
      });

      // Only keep tight phonetic matches or exact literal prefix matches
      const maxDist = Math.floor(pq.length / 4);
      const filtered = scored.filter(s => s.phonDist <= maxDist || s.score >= 100);
      return filtered.slice(0, 12);
    }

    function levenshtein(a, b) {
      const m = a.length, n = b.length;
      const dp = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));
      for (let i = 0; i <= m; i++) dp[i][0] = i;
      for (let j = 0; j <= n; j++) dp[0][j] = j;
      for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
          dp[i][j] = Math.min(
            dp[i - 1][j] + 1,
            dp[i][j - 1] + 1,
            dp[i - 1][j - 1] + (a[i - 1] !== b[j - 1] ? 1 : 0)
          );
        }
      }
      return dp[m][n];
    }

    function catClass(cat) { return 'cat cat-' + cat; }
    function genderLabel(g) { return g === 'm' ? 'masculin' : g === 'f' ? 'féminin' : ''; }

    // Highlight differences between user input and matched word
    function highlightDiff(word, query) {
      if (!query) return word;
      const w = word.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
      const q = query.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');

      // Use Levenshtein backtrack to get char-level alignment
      const m = q.length, n = w.length;
      const dp = Array.from({ length: m + 1 }, () => Array(n + 1).fill(0));
      for (let i = 0; i <= m; i++) dp[i][0] = i;
      for (let j = 0; j <= n; j++) dp[0][j] = j;
      for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
          dp[i][j] = Math.min(
            dp[i - 1][j] + 1,
            dp[i][j - 1] + 1,
            dp[i - 1][j - 1] + (q[i - 1] !== w[j - 1] ? 1 : 0)
          );
        }
      }

      // Backtrack to classify each character in word
      const status = new Array(n).fill('same'); // 'same', 'change', 'add'
      let i = m, j = n;
      while (i > 0 || j > 0) {
        if (i > 0 && j > 0 && dp[i][j] === dp[i-1][j-1] + (q[i-1] !== w[j-1] ? 1 : 0)) {
          if (q[i-1] !== w[j-1]) status[j-1] = 'change';
          i--; j--;
        } else if (j > 0 && dp[i][j] === dp[i][j-1] + 1) {
          status[j-1] = 'add';
          j--;
        } else {
          i--;
        }
      }

      // Build highlighted HTML using original (accented) word chars
      let html = '';
      for (let k = 0; k < word.length; k++) {
        const cls = status[k] || 'same';
        html += `<span class="diff-${cls}">${word[k]}</span>`;
      }
      return html;
    }


    function showCard(entry, query) {
      const genderHtml = entry.gender
        ? `<span class="card-gender">${genderLabel(entry.gender)}</span>` : '';
      const phoneticVal = phonetic(entry.word);
      const wordHtml = query ? highlightDiff(entry.word, query) : entry.word;
      document.getElementById('result').innerHTML = `
        <div class="card">
          <div class="card-header">
            <div class="card-word">${wordHtml}</div>
            <button class="accept-btn" onclick="acceptWord('${entry.word.replace(/'/g, "\\'")}')" title="Accepter">✓</button>
          </div>
          <div class="card-meta">
            <span class="${catClass(entry.category)}">${entry.category}</span>
            ${genderHtml}
            <span class="phonetic-badge">/${phoneticVal}/</span>
          </div>
          <div class="card-definition">${entry.definition}</div>
          <div class="card-example">${entry.example}</div>
        </div>
      `;
    }

    function showResults(scored, query) {
      const resultEl = document.getElementById('result');
      const othersEl = document.getElementById('others');

      if (!scored.length) {
        resultEl.innerHTML = '';
        othersEl.innerHTML = '';
        return;
      }

      // Keep a mutable display order so we can swap
      const display = scored.slice(0, 5);
      renderResults(display, query);
    }

    function renderResults(display, query, swapIdx) {
      const resultEl = document.getElementById('result');
      const othersEl = document.getElementById('others');

      showCard(display[0].entry, query);
      if (swapIdx !== undefined) {
        const card = resultEl.querySelector('.card');
        if (card) card.classList.add('swap-in');
      }

      const runners = display.slice(1);
      if (runners.length) {
        othersEl.innerHTML = runners.map((s, i) => `
          <div class="mini-card" data-idx="${i}">
            <div class="word">${highlightDiff(s.entry.word, query)}</div>
          </div>`).join('');
        // Apply bounce-down animation to the card that was demoted
        if (swapIdx !== undefined) {
          const demotedEl = othersEl.children[swapIdx - 1];
          if (demotedEl) demotedEl.classList.add('swap-in');
        }
        othersEl.querySelectorAll('.mini-card').forEach(el => {
          el.addEventListener('click', () => {
            const idx = +el.dataset.idx + 1;
            // Swap clicked item to primary position
            const clicked = display[idx];
            display[idx] = display[0];
            display[0] = clicked;
            renderResults(display, query, idx);
            fitToScreen();
          });
        });
      } else {
        othersEl.innerHTML = '';
      }
    }

    // --- Auto-fit: progressively shrink if content overflows viewport ---
    function fitToScreen() {
      const main = document.querySelector('.main-content');
      let scale = 100;
      main.style.fontSize = '';
      while (main.scrollHeight > window.innerHeight && scale > 50) {
        scale -= 2;
        main.style.fontSize = scale + '%';
      }
    }
    window.addEventListener('resize', fitToScreen);

    // --- Sound effects (Web Audio API, no files needed) ---
    const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

    function playAcceptSound() {
      const now = audioCtx.currentTime;
      // Ascending sci-fi chime
      [440, 660, 880].forEach((freq, i) => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(freq, now + i * 0.08);
        gain.gain.setValueAtTime(0.15, now + i * 0.08);
        gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.08 + 0.3);
        osc.connect(gain).connect(audioCtx.destination);
        osc.start(now + i * 0.08);
        osc.stop(now + i * 0.08 + 0.3);
      });
    }

    function playTrophySound() {
      const now = audioCtx.currentTime;
      // Sparkly fanfare for exact match
      [523, 659, 784, 1047].forEach((freq, i) => {
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(freq, now + i * 0.1);
        gain.gain.setValueAtTime(0.18, now + i * 0.1);
        gain.gain.exponentialRampToValueAtTime(0.001, now + i * 0.1 + 0.4);
        osc.connect(gain).connect(audioCtx.destination);
        osc.start(now + i * 0.1);
        osc.stop(now + i * 0.1 + 0.4);
      });
    }

    // --- Game answer sound effects ---
    function playCorrectSound() {
      const now = audioCtx.currentTime;
      // Triumphant ascending major arpeggio
      [523.25, 659.25, 783.99, 1046.5].forEach((freq, i) => {
        const osc = audioCtx.createOscillator();
        const g = audioCtx.createGain();
        osc.type = 'sine';
        osc.frequency.value = freq;
        g.gain.setValueAtTime(0.2, now + i * 0.07);
        g.gain.exponentialRampToValueAtTime(0.001, now + i * 0.07 + 0.35);
        osc.connect(g).connect(audioCtx.destination);
        osc.start(now + i * 0.07);
        osc.stop(now + i * 0.07 + 0.4);
      });
      // Bright shimmer on top
      const shimmer = audioCtx.createOscillator();
      const sg = audioCtx.createGain();
      shimmer.type = 'triangle';
      shimmer.frequency.value = 2093;
      sg.gain.setValueAtTime(0.1, now + 0.25);
      sg.gain.exponentialRampToValueAtTime(0.001, now + 0.8);
      shimmer.connect(sg).connect(audioCtx.destination);
      shimmer.start(now + 0.25);
      shimmer.stop(now + 0.85);
    }

    function playWrongSound() {
      const now = audioCtx.currentTime;
      // Descending minor second — dissonant buzzy feel
      [310, 280].forEach((freq, i) => {
        const osc = audioCtx.createOscillator();
        const g = audioCtx.createGain();
        osc.type = 'sawtooth';
        const filter = audioCtx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.value = 800;
        osc.frequency.value = freq;
        g.gain.setValueAtTime(0.15, now + i * 0.15);
        g.gain.exponentialRampToValueAtTime(0.001, now + i * 0.15 + 0.4);
        osc.connect(filter).connect(g).connect(audioCtx.destination);
        osc.start(now + i * 0.15);
        osc.stop(now + i * 0.15 + 0.45);
      });
    }

    function playGameEndSound(pct) {
      const now = audioCtx.currentTime;
      const dest = audioCtx.destination;

      if (pct >= 70) {
        // Grand victory celebration — multi-layered joyful fanfare

        // 1) Brass-like ascending fanfare (C major → high C)
        const fanfare = [261.63, 329.63, 392, 523.25, 659.25, 783.99, 1046.5];
        fanfare.forEach((freq, i) => {
          const osc = audioCtx.createOscillator();
          const g = audioCtx.createGain();
          const f = audioCtx.createBiquadFilter();
          osc.type = 'sawtooth';
          f.type = 'lowpass';
          f.frequency.value = 2500 + i * 200;
          osc.frequency.value = freq;
          g.gain.setValueAtTime(0.12, now + i * 0.08);
          g.gain.linearRampToValueAtTime(0.14, now + i * 0.08 + 0.1);
          g.gain.exponentialRampToValueAtTime(0.001, now + i * 0.08 + 1.2);
          osc.connect(f).connect(g).connect(dest);
          osc.start(now + i * 0.08);
          osc.stop(now + i * 0.08 + 1.3);
        });

        // 2) Sustained bright major chord (rings out after arpeggio)
        const chordStart = now + fanfare.length * 0.08;
        [523.25, 659.25, 783.99, 1046.5].forEach(freq => {
          const osc = audioCtx.createOscillator();
          const g = audioCtx.createGain();
          osc.type = 'triangle';
          osc.frequency.value = freq;
          g.gain.setValueAtTime(0, chordStart);
          g.gain.linearRampToValueAtTime(0.1, chordStart + 0.15);
          g.gain.exponentialRampToValueAtTime(0.001, chordStart + 2.0);
          osc.connect(g).connect(dest);
          osc.start(chordStart);
          osc.stop(chordStart + 2.1);
        });

        // 3) Sparkle shower — rapid high twinkles
        for (let i = 0; i < 12; i++) {
          const t = now + 0.3 + i * 0.12;
          const freq = 1800 + Math.random() * 2500;
          const osc = audioCtx.createOscillator();
          const g = audioCtx.createGain();
          osc.type = 'sine';
          osc.frequency.value = freq;
          g.gain.setValueAtTime(0.06 + Math.random() * 0.06, t);
          g.gain.exponentialRampToValueAtTime(0.001, t + 0.3);
          osc.connect(g).connect(dest);
          osc.start(t);
          osc.stop(t + 0.35);
        }

        // 4) Celebration boom
        const boom = audioCtx.createOscillator();
        const bg = audioCtx.createGain();
        boom.type = 'sine';
        boom.frequency.setValueAtTime(80, now);
        boom.frequency.exponentialRampToValueAtTime(30, now + 0.4);
        bg.gain.setValueAtTime(0.25, now);
        bg.gain.exponentialRampToValueAtTime(0.001, now + 0.5);
        boom.connect(bg).connect(dest);
        boom.start(now);
        boom.stop(now + 0.55);

      } else {
        // Warm encouraging melody — still uplifting, ascending end
        const melody = [261.63, 293.66, 329.63, 392, 523.25];
        melody.forEach((freq, i) => {
          const osc = audioCtx.createOscillator();
          const g = audioCtx.createGain();
          osc.type = 'triangle';
          osc.frequency.value = freq;
          g.gain.setValueAtTime(0.14, now + i * 0.18);
          g.gain.exponentialRampToValueAtTime(0.001, now + i * 0.18 + 0.6);
          osc.connect(g).connect(dest);
          osc.start(now + i * 0.18);
          osc.stop(now + i * 0.18 + 0.65);
        });
        // Gentle resolved chord at the end
        const cEnd = now + melody.length * 0.18;
        [392, 523.25].forEach(freq => {
          const osc = audioCtx.createOscillator();
          const g = audioCtx.createGain();
          osc.type = 'sine';
          osc.frequency.value = freq;
          g.gain.setValueAtTime(0.08, cEnd);
          g.gain.exponentialRampToValueAtTime(0.001, cEnd + 1.0);
          osc.connect(g).connect(dest);
          osc.start(cEnd);
          osc.stop(cEnd + 1.1);
        });
      }
    }

    // --- Game background music (procedural ambient space loop) ---
    let bgMusicNodes = null;

    function startBgMusic() {
      if (bgMusicNodes) return;
      const master = audioCtx.createGain();
      master.gain.setValueAtTime(0, audioCtx.currentTime);
      master.gain.linearRampToValueAtTime(0.18, audioCtx.currentTime + 1.5);
      master.connect(audioCtx.destination);

      const nodes = [];
      const intervals = [];

      // Power bass — rich sub with slight overdrive feel
      [55, 55.2, 110].forEach((freq, i) => {
        const osc = audioCtx.createOscillator();
        const g = audioCtx.createGain();
        osc.type = i < 2 ? 'sawtooth' : 'sine';
        osc.frequency.value = freq;
        g.gain.value = i < 2 ? 0.15 : 0.3;
        osc.connect(g).connect(master);
        osc.start();
        nodes.push(osc);
      });

      // Uplifting chord pad — major chord (C-E-G-B) with bright sawtooth + filter
      [261.63, 329.63, 392, 493.88].forEach((freq, i) => {
        const osc = audioCtx.createOscillator();
        const g = audioCtx.createGain();
        const filter = audioCtx.createBiquadFilter();
        const lfo = audioCtx.createOscillator();
        const lfoGain = audioCtx.createGain();
        osc.type = 'sawtooth';
        osc.frequency.value = freq;
        filter.type = 'lowpass';
        filter.frequency.value = 1200 + i * 200;
        filter.Q.value = 2;
        g.gain.value = 0.12;
        // Sweeping filter for movement
        lfo.type = 'sine';
        lfo.frequency.value = 0.25 + i * 0.08;
        lfoGain.gain.value = 400;
        lfo.connect(lfoGain).connect(filter.frequency);
        osc.connect(filter).connect(g).connect(master);
        lfo.start();
        osc.start();
        nodes.push(osc, lfo);
      });

      // Full drum kit — punchy four-on-the-floor with snare, open hats, and fills
      let beatPhase = 0;
      const bpm = 132;
      const beatMs = (60 / bpm / 2) * 1000; // eighth notes

      function synthDrum(type, freq, freqEnd, dur, vol, filterFreq) {
        const now = audioCtx.currentTime;
        const osc = audioCtx.createOscillator();
        const g = audioCtx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, now);
        if (freqEnd) osc.frequency.exponentialRampToValueAtTime(freqEnd, now + dur * 0.6);
        g.gain.setValueAtTime(vol, now);
        g.gain.exponentialRampToValueAtTime(0.001, now + dur);
        if (filterFreq) {
          const f = audioCtx.createBiquadFilter();
          f.type = type === 'square' ? 'highpass' : 'lowpass';
          f.frequency.value = filterFreq;
          f.Q.value = 1;
          osc.connect(f).connect(g).connect(master);
        } else {
          osc.connect(g).connect(master);
        }
        osc.start(now);
        osc.stop(now + dur + 0.01);
      }

      // Noise burst helper for snare / clap
      function noiseHit(dur, vol) {
        const now = audioCtx.currentTime;
        const bufSize = audioCtx.sampleRate * dur;
        const buf = audioCtx.createBuffer(1, bufSize, audioCtx.sampleRate);
        const data = buf.getChannelData(0);
        for (let i = 0; i < bufSize; i++) data[i] = Math.random() * 2 - 1;
        const src = audioCtx.createBufferSource();
        src.buffer = buf;
        const g = audioCtx.createGain();
        const f = audioCtx.createBiquadFilter();
        f.type = 'bandpass';
        f.frequency.value = 3000;
        f.Q.value = 0.8;
        g.gain.setValueAtTime(vol, now);
        g.gain.exponentialRampToValueAtTime(0.001, now + dur);
        src.connect(f).connect(g).connect(master);
        src.start(now);
      }

      const pulseInterval = setInterval(() => {
        if (!bgMusicNodes) { clearInterval(pulseInterval); return; }
        const beat = beatPhase % 8; // 8 eighth-notes = 1 bar

        // Kick on 1, 3, 5, 7 (four-on-the-floor quarter notes)
        if (beat % 2 === 0) {
          synthDrum('sine', 160, 35, 0.2, 0.35);
          // Layer a click transient for punch
          synthDrum('triangle', 800, 100, 0.03, 0.2);
        }

        // Snare on beats 2 and 6 (backbeat)
        if (beat === 2 || beat === 6) {
          synthDrum('triangle', 200, 120, 0.12, 0.2);
          noiseHit(0.15, 0.18);
        }

        // Clap layered with snare on beat 6 for emphasis
        if (beat === 6) {
          setTimeout(() => noiseHit(0.1, 0.12), 15);
        }

        // Open hi-hat on off-beats (1, 3, 5, 7)
        if (beat % 2 === 1) {
          synthDrum('square', 7000 + Math.random() * 2000, null, 0.08, 0.07, 6000);
        }

        // Closed hi-hat on on-beats
        if (beat % 2 === 0) {
          synthDrum('square', 8000 + Math.random() * 1500, null, 0.03, 0.05, 7500);
        }

        // Tom fill every 4 bars on the last 2 eighth notes
        if (beatPhase > 0 && beatPhase % 32 >= 30) {
          const tomFreq = beat >= 7 ? 100 : 140;
          synthDrum('sine', tomFreq * 1.5, tomFreq, 0.18, 0.2);
          noiseHit(0.06, 0.08);
        }

        // Crash cymbal every 4 bars on beat 0
        if (beatPhase > 0 && beatPhase % 32 === 0) {
          synthDrum('square', 5000, 2000, 0.6, 0.1, 3000);
          noiseHit(0.5, 0.1);
        }

        beatPhase++;
      }, beatMs);
      intervals.push(pulseInterval);

      // Arpeggiated synth — fast exciting runs
      let arpStep = 0;
      const arpNotes = [523.25, 659.25, 783.99, 1046.5, 783.99, 659.25];
      const arpInterval = setInterval(() => {
        if (!bgMusicNodes) { clearInterval(arpInterval); return; }
        const now = audioCtx.currentTime;
        const freq = arpNotes[arpStep % arpNotes.length];
        const osc = audioCtx.createOscillator();
        const g = audioCtx.createGain();
        const f = audioCtx.createBiquadFilter();
        osc.type = 'square';
        osc.frequency.value = freq;
        f.type = 'lowpass';
        f.frequency.value = 2500;
        g.gain.setValueAtTime(0.07, now);
        g.gain.exponentialRampToValueAtTime(0.001, now + 0.15);
        osc.connect(f).connect(g).connect(master);
        osc.start(now);
        osc.stop(now + 0.18);
        arpStep++;
      }, beatMs);
      intervals.push(arpInterval);

      // Sparkling high notes — bright twinkles
      const twinkleInterval = setInterval(() => {
        if (!bgMusicNodes) { clearInterval(twinkleInterval); return; }
        const freq = 1200 + Math.random() * 3000;
        const osc = audioCtx.createOscillator();
        const g = audioCtx.createGain();
        const now = audioCtx.currentTime;
        osc.type = 'sine';
        osc.frequency.value = freq;
        g.gain.setValueAtTime(0.06 + Math.random() * 0.05, now);
        g.gain.exponentialRampToValueAtTime(0.001, now + 0.4 + Math.random() * 0.3);
        osc.connect(g).connect(master);
        osc.start(now);
        osc.stop(now + 0.8);
      }, 300 + Math.random() * 200);
      intervals.push(twinkleInterval);

      bgMusicNodes = { master, nodes, intervals };
    }

    function stopBgMusic() {
      if (!bgMusicNodes) return;
      const { master, nodes, intervals } = bgMusicNodes;
      intervals.forEach(id => clearInterval(id));
      master.gain.linearRampToValueAtTime(0, audioCtx.currentTime + 1.5);
      setTimeout(() => {
        nodes.forEach(n => { try { n.stop(); } catch(e){} });
        master.disconnect();
      }, 1600);
      bgMusicNodes = null;
    }

    function acceptWord(word) {
      const inputText = document.getElementById('search').value.trim();
      if (inputText) {
        const isExact = inputText.toLowerCase() === word.toLowerCase();
        if (isExact) playTrophySound(); else playAcceptSound();
        const wordHtml = highlightDiff(word, inputText);
        acceptedPairs.push({ input: inputText, word: word });
        addPairCard(inputText, wordHtml, isExact);
      }
      document.getElementById('search').value = '';
      document.getElementById('result').innerHTML = '';
      document.getElementById('others').innerHTML = '';
      document.getElementById('search').focus();
      const hint = document.querySelector('.hint');
      if (hint) hint.style.display = '';
      fitToScreen();
    }

    function addPairCard(input, wordHtml, isExact) {
      const panel = document.getElementById('pairs-panel');
      const empty = panel.querySelector('.panel-empty');
      if (empty) empty.remove();
      const card = document.createElement('div');
      card.className = 'pair-card' + (isExact ? ' pair-exact' : '');
      card.dataset.word = acceptedPairs[acceptedPairs.length - 1].word;
      card.dataset.input = input;
      if (isExact) {
        card.innerHTML = `
          <span class="pair-trophy">🏆</span>
          <div class="pair-word pair-word-exact">${input}</div>
          <button class="pair-remove" onclick="event.stopPropagation(); this.parentElement.remove(); updatePairCount();" title="Retirer">✕</button>
        `;
      } else {
        card.innerHTML = `
          <div class="pair-input">${input}</div>
          <div class="pair-arrow">↓</div>
          <div class="pair-word">${wordHtml}</div>
          <button class="pair-remove" onclick="event.stopPropagation(); this.parentElement.remove(); updatePairCount();" title="Retirer">✕</button>
        `;
      }
      card.addEventListener('click', () => showPairDetail(card.dataset.word, card.dataset.input));
      panel.prepend(card);
      updatePairCount();
      fitToScreen();
    }

    function showPairDetail(word, input) {
      if (gameState) return;
      const entry = dictionary.find(e => e.word === word);
      if (!entry) return;
      showCard(entry, input);
      document.getElementById('others').innerHTML = '';
      const search = document.getElementById('search');
      if (search) search.value = input;
      fitToScreen();
    }

    function updatePairCount() {
      const panel = document.getElementById('pairs-panel');
      const count = panel.querySelectorAll('.pair-card').length;
      const status = document.querySelector('.panel-status');
      if (status) status.textContent = count > 0 ? count + ' mot' + (count > 1 ? 's' : '') : 'sys ready';
      const btn = document.getElementById('challenge-btn');
      if (btn) btn.disabled = count < 2;
      if (count === 0) {
        panel.innerHTML = '<div class="panel-empty">Aucun mot accepté</div>';
        acceptedPairs = [];
      }
      fitToScreen();
    }

    // --- Challenge Game ---
    let gameState = null;

    function startChallenge() {
      if (acceptedPairs.length < 2) return;
      gameState = {
        pairs: shuffle([...acceptedPairs]),
        current: 0,
        score: 0,
        total: acceptedPairs.length
      };
      startBgMusic();
      showGameQuestion();
    }

    function shuffle(arr) {
      for (let i = arr.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [arr[i], arr[j]] = [arr[j], arr[i]];
      }
      return arr;
    }

    function getDistractors(correctWord, count) {
      // Generate plausible-looking but INVALID French spellings
      // by swapping common orthographic patterns
      const swaps = [
        [/eau/g, 'o'], [/eau/g, 'au'], [/eau/g, 'ot'],
        [/au/g, 'o'], [/au/g, 'eau'], [/au/g, 'ot'],
        [/ph/g, 'f'], [/f/g, 'ph'],
        [/qu/g, 'k'], [/qu/g, 'c'], [/c(?=[aou])/g, 'k'], [/k/g, 'qu'],
        [/ch/g, 'sh'], [/sh/g, 'ch'],
        [/tion/g, 'sion'], [/sion/g, 'tion'],
        [/ai/g, 'è'], [/è/g, 'ai'], [/ei/g, 'ai'],
        [/é/g, 'er'], [/é/g, 'ez'], [/er$/g, 'é'], [/ez$/g, 'é'],
        [/an/g, 'en'], [/en/g, 'an'],
        [/in/g, 'ain'], [/ain/g, 'in'], [/ein/g, 'in'],
        [/on/g, 'om'], [/om/g, 'on'],
        [/ou/g, 'oo'], [/ou/g, 'u'],
        [/oi/g, 'oua'], [/oua/g, 'oi'],
        [/gn/g, 'ni'], [/ni(?=[aeou])/g, 'gn'],
        [/ss/g, 's'], [/s(?=[aeiou])/g, 'ss'],
        [/ll/g, 'l'], [/l(?=[aeioué])/g, 'll'],
        [/tt/g, 't'], [/t(?=[aeioué])/g, 'tt'],
        [/mm/g, 'm'], [/m(?=[aeioué])/g, 'mm'],
        [/nn/g, 'n'], [/n(?=[aeioué])/g, 'nn'],
        [/gu(?=[ei])/g, 'g'], [/g(?=[ei])/g, 'gu'],
        [/ge(?=[ao])/g, 'j'], [/j/g, 'ge'],
        [/x$/g, 's'], [/s$/g, 'x'],
        [/t$/g, ''], [/$/, 't'],  // silent trailing t
        [/s$/g, ''], [/$/, 's'],  // silent trailing s
      ];

      const dictSet = new Set(dictionary.map(e => e.word.toLowerCase()));
      const results = new Set();
      const word = correctWord.toLowerCase();

      // Try each swap pattern
      for (const [pattern, replacement] of swaps) {
        if (results.size >= count * 3) break;
        if (pattern.test(word)) {
          const variant = word.replace(pattern, replacement);
          if (variant !== word && !dictSet.has(variant) && variant.length >= 2) {
            results.add(variant);
          }
        }
      }

      // If not enough, also try the user's original input as a distractor (if invalid)
      // and simple letter swaps
      if (results.size < count) {
        for (let i = 0; i < word.length - 1 && results.size < count * 3; i++) {
          const arr = word.split('');
          [arr[i], arr[i + 1]] = [arr[i + 1], arr[i]];
          const variant = arr.join('');
          if (variant !== word && !dictSet.has(variant)) results.add(variant);
        }
      }

      // Pick random subset, capitalize to match
      const capitalize = s => correctWord[0] === correctWord[0].toUpperCase()
        ? s.charAt(0).toUpperCase() + s.slice(1) : s;
      const arr = shuffle([...results]).slice(0, count);
      return arr.map(capitalize);
    }

    function showGameQuestion() {
      const main = document.querySelector('.main-content');
      const gs = gameState;

      if (gs.current >= gs.total) {
        showGameEnd();
        return;
      }

      const pair = gs.pairs[gs.current];
      const inputIsCorrect = pair.input.toLowerCase() === pair.word.toLowerCase();
      const numGenerated = inputIsCorrect ? 3 : 2;
      const distractors = getDistractors(pair.word, numGenerated);
      if (!inputIsCorrect) {
        distractors.unshift(pair.input);
      }
      const choices = shuffle([pair.word, ...distractors.slice(0, 3)]);

      main.innerHTML = `
        <div class="game-container">
          <div class="game-score">Question ${gs.current + 1} / ${gs.total} · Score: ${gs.score}</div>
          <div class="game-prompt">Quel mot avais-tu choisi ?</div>
          <div class="game-choices">
            ${choices.map(c => `<button class="game-choice" onclick="checkAnswer(this, '${c.replace(/'/g, "\\'")}', '${pair.word.replace(/'/g, "\\'")}')">${c}</button>`).join('')}
          </div>
          <div class="game-feedback" id="game-feedback"></div>
          <button class="game-exit" onclick="exitChallenge()">✕ Quitter</button>
        </div>
      `;
      fitToScreen();
    }

    function checkAnswer(btn, chosen, correct) {
      const buttons = btn.parentElement.querySelectorAll('.game-choice');
      buttons.forEach(b => {
        b.disabled = true;
        if (b.textContent === correct) b.classList.add('correct');
        else if (b === btn && chosen !== correct) b.classList.add('wrong');
      });

      const feedback = document.getElementById('game-feedback');
      if (chosen === correct) {
        gameState.score++;
        playCorrectSound();
        feedback.innerHTML = '<span style="color:#4ade80">✨ Bravo !</span>';
      } else {
        playWrongSound();
        feedback.innerHTML = `<span style="color:#ff6b6b">C'est <strong>${correct}</strong></span>`;
      }

      setTimeout(() => {
        gameState.current++;
        showGameQuestion();
      }, 1500);
    }

    function showGameEnd() {
      stopBgMusic();
      const main = document.querySelector('.main-content');
      const gs = gameState;
      const pct = Math.round((gs.score / gs.total) * 100);
      playGameEndSound(pct);
      const emoji = pct === 100 ? '🏆' : pct >= 70 ? '⭐' : pct >= 40 ? '🚀' : '💪';

      main.innerHTML = `
        <div class="game-end">
          <div class="game-end-emoji">${emoji}</div>
          <div class="game-end-score">${gs.score} / ${gs.total}</div>
          <div class="game-prompt">${pct === 100 ? 'Parfait !' : pct >= 70 ? 'Très bien !' : pct >= 40 ? 'Bon effort !' : 'Continue !'}</div>
          <div style="display:flex; gap:0.8rem; margin-top:1rem;">
            <button class="game-next" onclick="startChallenge()">🔄 Rejouer</button>
            <button class="game-next" onclick="exitChallenge()">← Retour</button>
          </div>
        </div>
      `;
      fitToScreen();
    }

    function exitChallenge() {
      gameState = null;
      stopBgMusic();
      const main = document.querySelector('.main-content');
      main.innerHTML = `
        <div class="title">Astermots</div>
        <div class="subtitle-text">Dictionnaire phonétique interstellaire d'Orion</div>
        <div class="search-container">
          <input type="text" id="search" placeholder="Écris comme tu entends…" autocomplete="off" autofocus>
        </div>
        <div id="result"></div>
        <div class="bottom-row" id="others"></div>
        <p class="hint">Essaie : <code>gato</code> → gâteau · <code>xien</code> → chien · <code>garson</code> → garçon · <code>foto</code> → photo</p>
      `;
      // Re-wire search events
      wireSearchEvents();
      fitToScreen();
    }

    // --- Event wiring ---
    let currentScored = [];

    function wireSearchEvents() {
      const searchEl = document.getElementById('search');
      searchEl.addEventListener('input', () => {
        activeIndex = -1;
        const q = searchEl.value.trim();
        currentScored = searchWords(q);
        showResults(currentScored, q);
        fitToScreen();

        const hint = document.querySelector('.hint');
        if (hint) hint.style.display = q.length > 0 ? 'none' : '';
      });

      searchEl.addEventListener('keydown', (e) => {
        if (!currentScored.length) return;
        const top5 = currentScored.slice(0, 5);
        if (e.key === 'ArrowDown') {
          e.preventDefault();
          activeIndex = Math.min(activeIndex + 1, top5.length - 1);
          showCard(top5[activeIndex].entry, searchEl.value.trim());
        } else if (e.key === 'ArrowUp') {
          e.preventDefault();
          activeIndex = Math.max(activeIndex - 1, 0);
          showCard(top5[activeIndex].entry, searchEl.value.trim());
        }
      });
    }

    wireSearchEvents();

    // --- Load dictionary ---
    fetch('src/data/dictionary.json')
      .then(r => r.json())
      .then(data => {
        dictionary = data.map(e => ({ ...e, _phonetic: phonetic(e.word) }));
        document.getElementById('search').focus();
      })
      .catch(err => {
        console.error(err);
      });
  