from flask import Flask, render_template, request

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True

# Dictionary untuk satuan
units = {"celsius": "°C", "fahrenheit": "°F", "kelvin": "K", "rankine": "R"}

# Dictionary untuk rumus-rumus
formulas = {
    "celsius": {
        "fahrenheit": "{degrees}°C × 9/5 + 32",
        "kelvin": "{degrees}°C + 273.15",
        "rankine": "({degrees}°C + 273.15) × 9/5"
    },
    "fahrenheit": {
        "celsius": "({degrees}°F - 32) × 5/9",
        "kelvin": "({degrees}°F + 459.67) × 5/9",
        "rankine": "{degrees}°F + 459.67"
    },
    "kelvin" : {
        "celsius": "{degrees}K - 273.15",
        "fahrenheit": "{degrees}K × 9/5 - 459.67",
        "rankine": "{degrees}K × 9/5"
    },
    "rankine" : {
        "celsius": "{degrees}°R × 5/9 - 273.15",
        "fahrenheit": "{degrees}°R - 459.67",
        "kelvin": "{degrees}°R × 5/9"
    }
}

# Route home page
@app.route("/")
def index():
    return render_template("index.html")

# Route halaman temperature converter
@app.route("/temp_convert", methods=["GET", "POST"])
def convert():
    if request.method == "POST":
        # Satuan awal dan akhir, dicek jika ada atau termasuk satuan valid
        fromUnit = request.form.get("fromUnit")
        toUnit = request.form.get("toUnit")
        for unit in [fromUnit, toUnit]:
            if not unit or unit not in units:
                error = "Please enter a valid unit!"
                return render_template("temp_convert.html", error=error)

        # Derajat
        try:
            degrees = float(request.form.get("degrees"))
        except ValueError:
            value_error = "Please enter a value!"
            return render_template("temp_convert.html", value_error=value_error)

        # Jike satuan awal dan akhir sama, tidak akan dilakukan perhitungan
        if fromUnit == toUnit:
            result = degrees
            return render_template("temp_convert.html", result=result, fromUnit=fromUnit, toUnit=toUnit, degrees=degrees, units=units)

        # Konversi akan dilakukan dengan function
        result = conversion(fromUnit, toUnit, degrees)

        # Pemasukan rumus yang akan ditampilkan sesuai dengan satuan awal dan akhir
        calculations = formulas[fromUnit][toUnit].format(degrees=degrees)

        return render_template("temp_convert.html", result=result, fromUnit=fromUnit, toUnit=toUnit, degrees=degrees, units=units, calculations=calculations)
    else:
        return render_template('temp_convert.html')

# Function untuk mengkonversi suhu
def conversion(fromUnit, toUnit, degrees):
    # Agar lebih singkat, semua input akan dijadikan kelvin terlebih dahulu, kemudian dilanjutkan sesuai satuan akhirnya
    if fromUnit != "kelvin":
        if fromUnit == "celsius":
            degrees = degrees + 273.15
        elif fromUnit == "fahrenheit":
            degrees = (degrees + 459.67) * 5/9
        elif fromUnit == "rankine":
            degrees = degrees * 5/9

    if toUnit == "celsius":
        return degrees - 273.15
    elif toUnit == "fahrenheit":
        return degrees * 9/5 - 459.67
    elif toUnit == "rankine":
        return degrees * 9/5
    elif toUnit == "kelvin":
        return degrees
