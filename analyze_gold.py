from tvdatafeed import TvDatafeed, Interval
import pandas as pd
import ta

# تسجيل الدخول (أو اترك الحقول فارغة لاستخدام الجلسة العامة)
tv = TvDatafeed()

# جلب بيانات الذهب XAUUSD (دقيقة واحدة، آخر 500 شمعة)
df = tv.get_hist(symbol='XAUUSD', exchange='OANDA', interval=Interval.in_1_minute, n_bars=500)

# التأكد من نجاح الجلب
if df is None or df.empty:
    print("❌ لم يتم جلب بيانات XAUUSD.")
    exit()

# حساب المتوسطات المتحركة
df['ema20'] = ta.trend.ema_indicator(df['close'], window=20).ema_indicator()
df['ema50'] = ta.trend.ema_indicator(df['close'], window=50).ema_indicator()

# تحديد آخر صف للبيانات
latest = df.iloc[-1]

# تحليل الاتجاه
if latest['ema20'] > latest['ema50']:
    trend = "📈 الاتجاه صاعد (EMA20 > EMA50)"
else:
    trend = "📉 الاتجاه هابط (EMA20 < EMA50)"

# حساب مؤشر الزخم RSI
df['rsi'] = ta.momentum.RSIIndicator(df['close']).rsi()
rsi_value = df['rsi'].iloc[-1]

# طباعة التقرير
print("📊 تقرير فني لزوج XAUUSD:")
print(f"🕒 التاريخ والوقت: {latest.name}")
print(f"💰 الإغلاق: {latest['close']:.2f}")
print(f"{trend}")
print(f"📌 مؤشر القوة النسبية (RSI): {rsi_value:.2f}")
