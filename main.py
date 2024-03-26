import pandas as pd
import datetime
import numpy as np
from pandas.tseries.offsets import Second
from yfinance.utils import auto_adjust
import private
import settings
import yfinance as yf
import warnings
import os
import requests
import time
warnings.filterwarnings('ignore')

class signals:

    def macd_signal(self,Source, FastLength, SlowLength,  SignalLength):
        exp1 = Source.ewm(span=FastLength, adjust=False).mean()
        exp2 = Source.ewm(span=SlowLength, adjust=False).mean()
        macd = exp1-exp2
        signal = macd.ewm(span=SignalLength, adjust=False).mean()
        return pd.DataFrame({'macd': macd, 'signal': signal, })
    def williams(self,location):
        #calculate williams_%R
        if self.data.shape[0]<settings.setting.williams_period:
            return None
        williams=(self.data['High'].iloc[-location:-(settings.setting.williams_period+location):-1].max()-self.data['Close'].iloc[-1])/ \
            (self.data['High'].iloc[-location:-(settings.setting.williams_period+location):-1].max()\
                -self.data['Low'].iloc[-location:-(settings.setting.williams_period+location):-1].min())
        return -williams*100
    def macd_status(self,result):
        '''
        This method is used to calculate mcd_status by using macd and signal indicators
        Parameters:
        result:-Dataframe dataframe that contains macd and signal data.
        '''
        action_status= ''
        relative_status= ''
        current_macd=result['macd'].iloc[-1] 
        previous_macd=result['macd'].iloc[-2] 
        current_signal=result['signal'].iloc[-1]
        # calculate buy and hold action status
        if current_macd > current_signal:
            if (current_macd < 0 and current_signal < 0) and (previous_macd < current_signal):
                    action_status= 'BUY'
            else:
                action_status= 'HOLD'
        # calculate sell and stay out
        if current_macd < current_signal:
            if (current_macd > 0 and current_signal > 0) and ( previous_macd> current_signal):
                action_status= 'SELL'
            else:
                action_status= 'STAY OUT'
        # calculate crossed down and crossed up relative status
        if (np.sign(previous_macd)*np.sign(current_macd) == -1):
                if np.sign(current_macd) == -1:
                    relative_status= 'CROSSED DOWN'
                else:
                    relative_status = 'CROSSED UP'
        # calculate above 0 and below 0 relative status
        elif current_macd > 0:
                relative_status= 'Above 0'
        elif current_macd < 0:
                relative_status = 'Below 0'

        return action_status,relative_status
    def williams_status(self):
        '''
        Is used to calculate williams_%R status using williams indicator and overbought and oversold lines
        '''
        current=self.williams(1)
        previous=self.williams(2)
        # calculate buy and stay out status
        if current is None or previous is None:
            return 'NA'
        if current>settings.setting.overSold:
            if previous<settings.setting.overSold:
                return 'BUY'
        else:
            return 'STAY OUT'
            
        # calculate sell and hold status
        if current<settings.setting.overBought:
            if previous>settings.setting.overBought:
                return 'SELL'
        else:
            return 'HOLD'
        
        return 'NON'
    def write_to_google_sheet(self,data,Sheet):
        while True:
            try:
                client = private.authorize('client_secret.json')
                trading = client.open("TRADING")
                sheet = trading.worksheet(Sheet)
                trading.values_clear(f"{Sheet}!A1:W{len(settings.setting.ticker*2)+1}")
                sheet.insert_row(list(data.columns))
                send = []
                for row in data.values:
                    send.append(list(row))
                sheet.insert_rows(send, row=2)
                break
            except:
                print('authentication error at writing')
                time.sleep(2)
        
    
    def read_from_google_sheet(self,sheet):
        while True:
            try:
                client = private.authorize('client_secret.json')
                sheet = client.open("TRADING").worksheet(sheet)
                data=sheet.get_all_records()
                final_instruction = pd.DataFrame(data)
                return final_instruction
            except:
                print('authentication error at reading')
                time.sleep(2)
    def signal(self):
        result = pd.DataFrame(columns=['INSTRUMENT', 'INDICATOR','1M','1M(R)',
                                       '1W','1W(R)','1D','1D(R)','SHORT-INSTRUCTION','LONG-INSTRUCTION'])
        final_instruction = self.read_from_google_sheet('Instruction')
        
        for ticker in settings.setting.ticker:

            macd = {'INSTRUMENT': ticker,
                     'INDICATOR': 'MACD'}
            williams_r={'INSTRUMENT': '',
                     'INDICATOR': '%R',
                     '1M(R)':'',
                     '1W(R)':'',
                     '1D(R)':'',
                     'SHORT-INSTRUCTION':'',
                     'LONG-INSTRUCTION':''
            }
            for interval in ['1mo', '1wk', '1d']:
                if interval in ['1d','1wk','1mo']:
                    period='7y'
                elif interval=='1m':
                    period='7d'
                else:
                    period='30d'
                Ticker = yf.Ticker(ticker)
                while 1:
                    try:
                        self.data = Ticker.history(period=period,interval=interval)
                        break
                    except:
                        print('Error from the yahoo side')
                        time.sleep(5)
                try:
                    action_status,relative_status = self.macd_status(self.macd_signal(self.data[settings.setting.Source], settings.setting.macd_fastLength,
                                               settings.setting.macd_slowLength, settings.setting.macd_signalLength))
                except IndexError:
                    print(f'Only one row for ticker {ticker} and interval {interval}')
                    return
                williams=self.williams_status()
                if interval=='1d':
                    macd['1D'] = action_status
                    macd['1D(R)'] = relative_status
                    williams_r['1D']=williams
                elif interval=='1wk':
                    macd['1W'] = action_status
                    macd['1W(R)'] = relative_status
                    williams_r['1W']=williams

                elif interval == '1h':
                    macd['1H'] = action_status
                    macd['1H(R)'] = relative_status
                    williams_r['1H'] = williams
                elif interval=='1mo':
                    macd['1M'] = action_status
                    macd['1M(R)'] = relative_status
                    williams_r['1M'] = williams
                elif interval=='30m':
                    macd['30m'] = action_status
                    macd['30m(R)'] = relative_status
                    williams_r['30m'] = williams
                elif interval=='15m':
                    macd['15m'] = action_status
                    macd['15m(R)'] = relative_status
                    williams_r['15m'] = williams
                elif interval=='5m':
                    macd['5m'] = action_status
                    macd['5m(R)'] = relative_status
                    williams_r['5m'] = williams
                elif interval=='2m':
                    macd['2m'] = action_status
                    macd['2m(R)'] = relative_status
                    williams_r['2m'] = williams
                else:
                    macd['1m'] = action_status
                    macd['1m(R)'] = relative_status
                    williams_r['1m'] = williams
                # Determine the final status
                if interval in settings.setting.instruction_period:
                    instruction='LONG-INSTRUCTION'
                    if interval==settings.setting.instruction_period[0]:
                        instruction='SHORT-INSTRUCTION'
                    if not final_instruction[(final_instruction['MACD-Action']==action_status) &
                    (final_instruction['MACD-Relative']==relative_status) & (final_instruction['Williams']==williams)].empty:
                        macd[instruction]=final_instruction[(final_instruction['MACD-Action']==action_status) &
                                                              (final_instruction['MACD-Relative']==relative_status) & (final_instruction['Williams']==williams)]['Action'].iloc[0]
                                                        
                    else:
                        macd[instruction]='NA'    
            result = result.append(macd, ignore_index=True)
            result = result.append(williams_r, ignore_index=True)
        print(result)
        self.write_to_google_sheet(result,"Sheet1")
def entry(x,y):
    signal=signals()
    signal.signal()

