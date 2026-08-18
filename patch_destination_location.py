from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# Keep prior destination-location compatibility patching.
marker = '<div class="field wide locationBox"><label>موقعك الحالي للسائق</label>'
insert_after = '<div class="field wide locationBox"><label>موقع الوجهة التي تريد الذهاب إليها</label><input id="destinationLocation" placeholder="الصق رابط الموقع من Google Maps أو Apple Maps"><input id="destinationLocationText" style="margin-top:12px" placeholder="أو اكتب وصف موقع الوجهة: الحي، الشارع، رقم المبنى"><span class="hint">افتح المكان في تطبيق الخرائط واضغط مشاركة ثم انسخ الرابط والصقه هنا. سيظهر الرابط للسائق مع الحجز.</span></div>\n'
if 'id="destinationLocation"' not in s:
    pickup_block = '<div class="field wide locationBox"><label>موقعك الحالي للسائق</label><div class="locationRow"><button class="primary" type="button" onclick="shareLocation()">📍 إرسال موقعي الحالي</button><span id="locationStatus" class="locationStatus">لم يتم إرسال الموقع بعد.</span></div><input id="pickupText" style="margin-top:12px" placeholder="يمكنك أيضاً كتابة وصف للموقع: الحي، الشارع، رقم المبنى"><span class="hint">عند الضغط على «إرسال موقعي الحالي» سيطلب المتصفح إذنك للوصول للموقع.</span></div>\n'
    s = s.replace(pickup_block, pickup_block + insert_after)

# Definitive visual background fix: render the image as its own fixed layer ABOVE the page background,
# then keep all interface content above it. This avoids the old negative-z-index/fallback issue.
bg_css = '''
#siteVisualBg{position:fixed;inset:0;z-index:0;background-image:linear-gradient(180deg,rgba(0,0,0,.18),rgba(0,18,8,.44)),url("site-bg.jpg?v=9");background-size:cover;background-position:center top;background-repeat:no-repeat;pointer-events:none}
#siteVisualBg:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.02),rgba(0,8,4,.28) 58%,rgba(0,6,3,.55))}
.fallback{display:none!important}
body:before{display:none!important}
header,.hero,.heroStrip,.main,.page,.trust,footer{position:relative;z-index:2}
'''
if '#siteVisualBg{' not in s:
    s = s.replace('</style>', bg_css + '</style>', 1)

if 'id="siteVisualBg"' not in s:
    s = s.replace('<body>', '<body><div id="siteVisualBg" aria-hidden="true"></div>', 1)
    s = s.replace('<body><div class="fallback"></div>', '<body><div id="siteVisualBg" aria-hidden="true"></div><div class="fallback"></div>', 1)

# Disable the old JavaScript background loader if it exists; the fixed layer above is now authoritative.
needle = 'function loadBackground(){'
if needle in s:
    start = s.find(needle)
    brace = 0
    end = None
    for i in range(start, len(s)):
        if s[i] == '{':
            brace += 1
        elif s[i] == '}':
            brace -= 1
            if brace == 0:
                end = i + 1
                break
    if end:
        s = s[:start] + 'function loadBackground(){return;}' + s[end:]

p.write_text(s, encoding='utf-8')
