# 🧱 Print Friendly LEGO

This tool converts LEGO instruction manual PDFs (such as those used in the Botanicals Collection) into clean, print-friendly PNG images by:

1. **Converting PDF pages to high-resolution PNGs**
2. **Detecting and converting white-on-grey elements (e.g. arrows, step numbers) into black**
3. **Removing grey backgrounds** for clean output over white paper

---

## 📦 Features

- 🖨️ Converts white text/lines near the original grey background into black for improved print readability
- 🎯 Preserves white-filled callouts and graphics
- 🧼 Removes grey background (Defaults to #899093 range as used in the Botanicals Collection) last to prevent false positives
- 📄 Works on any PDF manual with grey backgrounds and white linework

---

## 📂 Folder Structure

After running the tool:

```bash

my\_manual.pdf
├── my\_manual\_raw\_png/         ← High-res PNGs from original PDF
└── my\_manual\_cleaned\_png/     ← Processed PNGs with background removed and lines/text converted

```

---

## 🚀 Usage

### 1. Install dependencies

```bash
pip install pillow pdf2image scipy
```

> **Note:** On Linux, you may also need `poppler`:
>
> ```bash
> sudo apt install poppler-utils
> ```

### 2. Run the script

```bash
python combined_print_friendly_lego.py path/to/my_manual.pdf
```

Optional:

```bash
--dpi 300       # Set DPI (default 300 for high quality)
--background-colour "#8A8A8A"   # Set a different background colour to remove (default #899093 )
```

---

## 🛠 How It Works

* **Grey Detection:** Uses a color distance threshold to detect background grey (#899093)
* **White Structure Conversion:** Finds white pixels adjacent to grey and converts their full connected components to black
* **Post-Processing:** Removes the grey pixels only at the end to avoid accidental over-conversion

---

## 📄 License

This project is licensed under the [GNU General Public License v3.0 (GPLv3)](https://www.gnu.org/licenses/gpl-3.0.en.html).

You are free to use, modify, and distribute this software, provided that:

* Any modifications are also shared under the GPLv3 license
* The source remains open

---

## 🤝 Contributions

Feel free to open issues or PRs!
