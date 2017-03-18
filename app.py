from flask import Flask, render_template, request, redirect
import quandl
from bokeh.plotting import figure
from bokeh.embed import components 

#app setup
app = Flask(__name__)
app.vars = {}
app.vars['checkbox'] = {}

#quandl setup
fin = open('apikey')
apikey = fin.readline().strip()
fin.close()
quandl.ApiConfig.api_key = apikey

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index',methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    else:
        #request was a POST
        print 'post recieved'
        ticker = request.form['ticker']
        features = request.form.getlist('features')

        #retrieve the data
        data = quandl.get("wiki/%s"%ticker, returns="pandas")

        #plot the data
        TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"
        plot = figure(title='Data from Quandle WIKI set',x_axis_label='Date',
              x_axis_type='datetime',tools=TOOLS)


        for ft,c in zip( ['Close','Adj. Close','Open','Adj. Open'], ['navy','red','green','yellow']):
            print ft,c
            if ft in features: 
                plot.line(data.index, data[ft], color=c,legend=ft)

        #plot.legend.orientation = "top_left" #doesn't want to work
        script, div = components(plot)
        return render_template('graph.html', script=script, div=div, ticker = ticker.upper())

#see http://blog.thedataincubator.com/2015/09/painlessly-deploying-data-apps-with-bokeh-flask-and-heroku/
#for the plotting code and templates

#see https://github.com/bev-a-tron/MyFlaskTutorial
#for a tutorial, understanding GET and POST from the website

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=33507)
