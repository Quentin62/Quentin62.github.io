import os

import pandas as pd

dat = pd.read_csv("./dedicace/Dédicace - Feuille 1.csv", parse_dates=["Année"], dayfirst=True)
dat["Album"] = dat["Album"].fillna("")

folder_img = "dedicace/"
for (serie, album), rows in dat.groupby(["Série", "Album"]):
    files = rows["Fichier"].sort_values()
    if len(files.dropna()) > 0:
        md_filename = os.path.splitext(os.path.basename(files.iloc[0]))[0] + ".md"
        html_filename = os.path.splitext(os.path.basename(files.iloc[0]))[0]

        date = rows["Année"].max()
        lieu = rows["Lieu"].iloc[0]

        md = '---\ntitle: "' + serie
        if album is not None:
            md += " : " + album
        md += '"\n'

        md += """collection: portfolio"""
        md += """\npermalink: /portfolio/""" + html_filename

        img = f"<img src='../{folder_img}{files.iloc[0]}'>"
        md += '\nexcerpt: "' + img + '"'

        md += "\ndate: " + date.strftime("%Y-%m-%d")

        md += "\n---"

        n_img = files.nunique()
        for file, dedicace in rows.groupby("Fichier"):
            for _, ded in dedicace.iterrows():
                md += "\n\nDédicace de : "
                md += ded["Auteur"] + " (" + ded["Lieu"] + ", " + ded["Année"].strftime("%Y") + ")"

                if not pd.isna(ded["Commentaire"]):
                    md += "<br>" + ded["Commentaire"]

            md += f"\n<img src='../{folder_img}{file}'>"

        with open("./_portfolio/" + md_filename, "w") as f:
            print(md_filename)
            f.write(md)
