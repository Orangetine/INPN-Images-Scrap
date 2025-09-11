import pandas as pd
import numpy as np
import os

IMAGES_PATH = "downloads/"
OUTPUT_DIR = "output/"

def reconstitution_t_medias_csv(chemin):
    image_files = os.listdir(IMAGES_PATH)
    t_medias = pd.read_csv("doc/t_medias.csv", sep=";")
    filenames_t_medias = [url.split("/")[-1] for url in t_medias["url"] if pd.notna(url)]
    filenames_downloads = [file.split(".")[0] for file in image_files]
    saved_images_nb = len(filenames_downloads)
    nb_images_initial = len(filenames_t_medias)

    print(f"Nombre d'images sauvées :",
          saved_images_nb,
          "Nombre d'images initial",
          nb_images_initial,
          "Taux de sauvegarde :",
          f"{round(saved_images_nb/nb_images_initial*100,2)}%", sep = "\n")
    t_medias["chemin"] = [
        f"{chemin}{url.split('/')[-1]}.jpg" 
        if (pd.notna(url) and url.split('/')[-1] in filenames_downloads)
        else np.nan 
        for url in t_medias["url"]
    ]
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    t_medias.to_csv(f"{OUTPUT_DIR}t_medias_final.csv", sep=";", index=False)
 

if __name__ == "__main__":
    reconstitution_t_medias_csv("static/custom/INPN_images/")