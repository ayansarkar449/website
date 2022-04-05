from website import raw_app
app = raw_app()
if __name__==  "__main__" :
        app.run(debug=False,host="0.0.0.0",port=80)
