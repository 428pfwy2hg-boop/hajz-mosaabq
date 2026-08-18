from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

marker = '<div class="field wide locationBox"><label>موقعك الحالي للسائق</label>'
insert_after = '<div class="field wide locationBox"><label>موقع الوجهة التي تريد الذهاب إليها</label><input id="destinationLocation" placeholder="الصق رابط الموقع من Google Maps أو Apple Maps"><input id="destinationLocationText" style="margin-top:12px" placeholder="أو اكتب وصف موقع الوجهة: الحي، الشارع، رقم المبنى"><span class="hint">افتح المكان في تطبيق الخرائط واضغط مشاركة ثم انسخ الرابط والصقه هنا. سيظهر الرابط للسائق مع الحجز.</span></div>\n'

if 'id="destinationLocation"' not in s:
    pickup_block = '<div class="field wide locationBox"><label>موقعك الحالي للسائق</label><div class="locationRow"><button class="primary" type="button" onclick="shareLocation()">📍 إرسال موقعي الحالي</button><span id="locationStatus" class="locationStatus">لم يتم إرسال الموقع بعد.</span></div><input id="pickupText" style="margin-top:12px" placeholder="يمكنك أيضاً كتابة وصف للموقع: الحي، الشارع، رقم المبنى"><span class="hint">عند الضغط على «إرسال موقعي الحالي» سيطلب المتصفح إذنك للوصول للموقع.</span></div>\n'
    s = s.replace(pickup_block, pickup_block + insert_after)

old_book = "let pickup=pickupText.value.trim();if(!dest||!d||!tm)"
new_book = "let pickup=pickupText.value.trim();let destLocation=destinationLocation.value.trim();let destLocationText=destinationLocationText.value.trim();if(!dest||!d||!tm)"
s = s.replace(old_book, new_book)

old_obj = "pickup,location:currentLocation,date:d,time:tm"
new_obj = "pickup,location:currentLocation,destinationLocation:destLocation,destinationLocationText:destLocationText,date:d,time:tm"
s = s.replace(old_obj, new_obj)

old_render = "</span></div><div><span class=\"status ${x.status==='ملغي'?'cancelled':''}\">"
new_render = "</span><br><span class=\"small\">موقع الوجهة: ${x.destinationLocationText||x.destination} ${x.destinationLocation?`· <a href=\"${x.destinationLocation}\" target=\"_blank\" style=\"color:#19c56b\">خريطة الوجهة</a>`:''}</span></div><div><span class=\"status ${x.status==='ملغي'?'cancelled':''}\">"
s = s.replace(old_render, new_render)

s = s.replace('أرسل موقعك الحالي للسائق، ثم أكّد الحجز المسبق', 'أرسل موقعك الحالي وموقع الوجهة للسائق، ثم أكّد الحجز المسبق')

# Use the real image committed as site-bg.jpg. This overrides the old broken base64 background.
if 'site-bg.jpg?v=6' not in s:
    css = '''body{background-image:linear-gradient(180deg,rgba(2,5,4,.22),rgba(2,6,4,.58)),url("site-bg.jpg?v=6")!important;background-size:cover!important;background-position:center top!important;background-repeat:no-repeat!important;background-attachment:fixed!important}body:before{background:linear-gradient(180deg,rgba(2,5,4,.08),rgba(2,6,4,.42) 72%,rgba(2,6,4,.70))!important}'''
    s = s.replace('</style>', css + '</style>', 1)

needle = 'function loadBackground(){'
if needle in s:
    replacement = '''function loadBackground(){document.body.style.backgroundImage="linear-gradient(180deg,rgba(2,5,4,.22),rgba(2,6,4,.58)),url('site-bg.jpg?v=6')";return;'''
    s = s.replace(needle, replacement, 1)

p.write_text(s, encoding='utf-8')
