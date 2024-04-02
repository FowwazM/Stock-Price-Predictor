from flask import Flask,request,render_template
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import io
import base64
from results import result

application=Flask(__name__)

app=application

# Route for the main page
@app.route('/',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('index.html')
    else:
        ticker=request.form.get('ticker')
        
        train, test, future_pred, mse, mape = result(ticker)
        rmse = np.sqrt(mse)

        # Plot the training data along with predictions against testing data
        fig = Figure(figsize=(10,8))
        result_plot = fig.add_subplot(1, 1, 1)
        result_plot.plot(train['Date'], train['Adj Close'])
        result_plot.plot(test['Date'], test[['Adj Close', 'Predictions']])
        result_plot.plot(future_pred['Date'], future_pred['Forecast'])
        result_plot.set_title(str(ticker) + ' Stock Close Price')
        result_plot.set_xlabel("Date")
        result_plot.set_ylabel("Price")
        result_plot.legend(['Train', 'Test', 'Predictions', 'Forecast'])

        # Convert plot to PNG image
        pngImage = io.BytesIO()
        FigureCanvas(fig).print_png(pngImage)
    
        # Encode PNG image to base64 string
        pngImageB64String = "data:image/png;base64,"
        pngImageB64String += base64.b64encode(pngImage.getvalue()).decode('utf8')

        # Render HTML page with model results
        return render_template('index.html', error=mse, rooterror=rmse, acc=(100 - mape), image=pngImageB64String)

if __name__=="__main__":
    app.run(host='0.0.0.0', port=8080)