"""
Baseline skup podataka

ideja je napraviti tabelu spremnu za model, koristeci samo podatke koji su poznati pre pocetka kursa (bez klikova na sajtu, bez ocena jer se to desava tek tokom kursa i nije poznato unapred).
"""

import pandas as pd
from oulad_pipe.data.loader import load_courses, load_student_info, load_student_registration

def build_baseline_dataset():
    student_info = load_student_info()
    courses = load_courses()
    registration = load_student_registration()

    student_info["at_risk"] = student_info["final_result"].isin(["Fail", "Withdrawn"])
    student_info["at_risk"] = student_info["at_risk"].astype(int)

    student_info = student_info.drop(columns=["final_result"])

    # Ako se student registrovao posle pocetka kursa (date_registration > 0), taj podatak se jos uvek ne zna u trenutku predikcije, treba ga sakriti
    registration.loc[registration["date_registration"] > 0, "date_registration"] = None

    #studentInfo + trajanje kursa (iz courses tabele)
    df = student_info.merge( courses[["code_module", "code_presentation", "module_presentation_length"]],
                            on=["code_module", "code_presentation"], how="left")

    # + datum registracije (iz registration tabele)
    df = df.merge(registration[["code_module", "code_presentation", "id_student", "date_registration"]],
                  on=["code_module", "code_presentation", "id_student"], how="left")

    return df


if __name__ == "__main__":
    dataset = build_baseline_dataset()
    dataset.to_csv("data/processed/baseline_dataset.csv", index=False)
    print(f"Baseline dataset: {dataset.shape}")