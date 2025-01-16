from app import db, constants
from flask import current_app, redirect, render_template, Blueprint, request, jsonify, url_for
from app.blueprints.map.forms import CoordinateForm
from app.models.locations import Location

bp_map = Blueprint(
    'map',
    __name__,
    template_folder='templates',
    static_folder='static',
    url_prefix='/map'
)

@bp_map.route('/', methods = ["GET", "POST"])
def map():

    coordinateForm = CoordinateForm()

    if request.method == "POST":

        # 获取到表单内容
        lng = coordinateForm.lng.data
        lat = coordinateForm.lat.data
        address = coordinateForm.address.data
        tag = coordinateForm.tag.data

        # 添加到数据库
        new_location = Location(lng, lat, address, tag)
        db.session.add(new_location)

        try:
            db.session.commit()
            current_app.logger.info("Location successfully added to the database.")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error committing to database: {e}")
            return jsonify({"error": str(e)}), 500

        return redirect(url_for('map.map'))

    else:
        # 获取所有位置数据
        locations = Location.query.all()
        return render_template("map.html", coordinateForm = coordinateForm, locations = locations, constants = constants)

@bp_map.route('/delete/<int:id>')
def delete(id):
    Location.query.filter(Location.id == id).delete()
    db.session.commit()
    return redirect(url_for('map.map'))
