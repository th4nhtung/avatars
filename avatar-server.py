import os
from pyfiglet import Figlet
from flask import Flask, send_file, jsonify
from subprocess import call
from sys import platform as _platform

if _platform == 'win32' or _platform == 'win64':
    call('cls', shell=True)
elif _platform == 'linux' or _platform == 'linux2':
    call('clear', shell=True)

f = Figlet(font='stop')
print(f.renderText('Avatar-Server'))

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 1

avatar_dir = "a"  # no slash

# create avatars directory if it does not exist
if not os.path.exists(os.path.join(app.root_path, avatar_dir)):
    os.makedirs(os.path.join(app.root_path, avatar_dir))

@app.route("/status")
def serverStatus():
    return jsonify({
        "response": 200,
        "status": 1
    })

@app.route("/<int:uid>")
def serveAvatar(uid):
    # Check if avatar exists
    if os.path.isfile(os.path.join(app.root_path, "{}/{}.png".format(avatar_dir, uid))):
        avatarid = uid
    else:
        avatarid = -1

    # Serve actual avatar or default one
    return send_file("{}/{}.png".format(avatar_dir, avatarid))

@app.errorhandler(404)
def page_not_found(error):
    return send_file("{}/-1.png".format(avatar_dir))

# Run the server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
