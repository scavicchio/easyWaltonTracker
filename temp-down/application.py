from flask import Flask, render_template, request, url_for, redirect

application = app = Flask(__name__)

@app.before_request
def check_for_maintenance():
    if request.path != url_for('maintenance'): 
        return redirect(url_for('maintenance'))
        # Or alternatively, dont redirect 
        # return 'Sorry, off for maintenance!', 503

@app.route('/maintenance')
def maintenance():
    return render_template('downsite.html')


# run the app.
if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    app.run(0.0.0.0,port=8080,debug=True)