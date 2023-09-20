import zipfile

# with zipfile.ZipFile("data_tdn_left.zip", "w") as zip_ref:
#     zip_ref.write("asd")
#     zip_ref.write("mnp")

fn = "data_tdn_left.zip"

with zipfile.ZipFile(fn, "r") as zip_ref:
    zip_ref.extractall()
