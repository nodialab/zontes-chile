# Iconos de trazo (24x24, currentColor). Un solo sprite por página + helper ic().
import re
I={
'engine':'<path d="M3 11h2V9h3V7h6v2h2l2 2h2v5h-2l-1 2H8l-1-2H5v-3H3z"/><path d="M10 13h4"/>',
'piston':'<rect x="7" y="3" width="10" height="9" rx="1.5"/><path d="M7 7h10M12 12v6M8 21h8M12 18l-4 3M12 18l4 3"/>',
'bolt':'<path d="M13 2L5 14h6l-1 8 8-12h-6z"/>',
'torque':'<path d="M20 12a8 8 0 1 1-2.4-5.7"/><path d="M20 4v4h-4"/><circle cx="12" cy="12" r="2"/>',
'gear':'<circle cx="12" cy="12" r="3.2"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M18.7 5.3l-2.1 2.1M7.4 16.6l-2.1 2.1"/>',
'drop':'<path d="M12 3c3.5 4.2 6 7 6 10.2A6 6 0 0 1 6 13.2C6 10 8.5 7.2 12 3z"/>',
'fuel':'<path d="M5 21V5a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v16M3 21h14M5 10h10"/><path d="M15 8h2a2 2 0 0 1 2 2v6a1.5 1.5 0 0 0 3 0V9l-3-3"/>',
'brake':'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="2.5"/><path d="M12 6.4v.01M17.6 12v.01M12 17.6v.01M6.4 12v.01"/>',
'abs':'<circle cx="12" cy="12" r="2.2"/><path d="M5 12a7 7 0 0 1 7-7M19 12a7 7 0 0 1-7 7M3.5 8.5A9.5 9.5 0 0 1 8.5 3.5M20.5 15.5a9.5 9.5 0 0 1-5 5"/>',
'tire':'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5.5"/><path d="M12 9v3.5M12 15.2v.01"/>',
'spring':'<path d="M12 2v3l5 2-10 3 10 3-10 3 5 2v4"/>',
'frame':'<circle cx="6" cy="17" r="3"/><circle cx="18" cy="17" r="3"/><path d="M6 17l3-8h6l3 8M9 9l-2-3h-2M13 9l1-3h3M10 17h4"/>',
'ruler':'<rect x="2" y="8" width="20" height="8" rx="1.5"/><path d="M6 8v3M10 8v4M14 8v3M18 8v4"/>',
'wheelbase':'<circle cx="5.5" cy="16" r="3"/><circle cx="18.5" cy="16" r="3"/><path d="M5.5 8h13M8 5.5L5.5 8 8 10.5M16 5.5l2.5 2.5-2.5 2.5"/>',
'weight':'<path d="M6.5 9h11l2 11h-15z"/><circle cx="12" cy="5.5" r="2.5"/>',
'seat':'<path d="M3 16c0-2 1.5-3 3.5-3h7l3-3h2a2 2 0 0 1 2 2v4"/><path d="M3 16h18M7 16v4M17 16v4"/>',
'height':'<path d="M12 3v18M8 7l4-4 4 4M8 17l4 4 4-4"/>',
'chain':'<circle cx="6" cy="12" r="4"/><circle cx="18" cy="12" r="2.2"/><path d="M6 8l12 1.8M6 16l12-1.8"/>',
'clutch':'<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5.5"/><circle cx="12" cy="12" r="1.5"/>',
'injection':'<path d="M12 3c2.7 3.3 4.5 5.4 4.5 7.7a4.5 4.5 0 0 1-9 0C7.5 8.4 9.3 6.3 12 3z"/><path d="M5 20h14M8 17v3M16 17v3"/>',
'key':'<circle cx="8" cy="15" r="4"/><path d="M11 12l9-9M16 7l3 3M14 9l2 2"/>',
'power':'<path d="M12 3v9"/><path d="M6.3 6.8a8 8 0 1 0 11.4 0"/>',
'light':'<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.6 10.8c.6.5 1.1 1.2 1.1 2V16h5v-.2c0-.8.5-1.5 1.1-2A6 6 0 0 0 12 3z"/>',
'usb':'<path d="M9 3v5M15 3v5M7 8h10v4a5 5 0 0 1-10 0zM12 17v4"/>',
'screen':'<rect x="3" y="5" width="18" height="12" rx="2"/><path d="M8 21h8M12 17v4"/>',
'gauge':'<path d="M4 18a8 8 0 1 1 16 0"/><path d="M12 18l4-5M7 12.5v.01M12 8.5v.01M17 12.5v.01"/>',
'lock':'<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3M12 15v2"/>',
'windshield':'<path d="M4 20c1-8 4-13 9-16l2 2c-2 3-3 7-3 14M4 20h12"/>',
'box':'<rect x="3" y="8" width="18" height="12" rx="2"/><path d="M8 8V6a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 13h18M11 13v2h2v-2"/>',
'flame':'<path d="M12 3c1 4 5 5.5 5 10a5 5 0 0 1-10 0c0-2 1-3 2-4 0 2 1 3 2 3 0-3-1-5 1-9z"/>',
'traction':'<circle cx="12" cy="12" r="3"/><path d="M12 3a9 9 0 0 1 9 9M12 21a9 9 0 0 1-9-9M18 3h3v3M6 21H3v-3"/>',
'modes':'<path d="M4 7h9M17 7h3M4 17h3M11 17h9"/><circle cx="15" cy="7" r="2"/><circle cx="9" cy="17" r="2"/>',
'parking':'<circle cx="12" cy="12" r="9"/><path d="M10 16V8h3a2.5 2.5 0 0 1 0 5h-3"/>',
'bluetooth':'<path d="M7 7l10 10-5 4V3l5 4L7 17"/>',
'shield':'<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="M9 12l2 2 4-4"/>',
'wrench':'<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.2-.6-.6-2.2z"/>',
'pin':'<path d="M12 21s7-6 7-11a7 7 0 0 0-14 0c0 5 7 11 7 11z"/><circle cx="12" cy="10" r="2.5"/>',
'phone':'<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
'mail':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
'chat':'<path d="M4 20l1.5-4.5A8 8 0 1 1 9 19z"/>',
'download':'<path d="M12 3v12M7 10l5 5 5-5M4 20h16"/>',
'arrow':'<path d="M5 12h14M13 6l6 6-6 6"/>',
'check':'<path d="M5 12l5 5 9-10"/>',
'clock':'<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
'globe':'<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c3 3 3 15 0 18M12 3c-3 3-3 15 0 18"/>',
'award':'<circle cx="12" cy="9" r="5"/><path d="M9 13.5L8 21l4-2 4 2-1-7.5"/>',
'phone-app':'<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>',
'file':'<path d="M6 3h8l5 5v13H6z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
'moto':'<circle cx="5.5" cy="16.5" r="3"/><circle cx="18.5" cy="16.5" r="3"/><path d="M5.5 16.5L9 9h5l2 3.5M14 9l-1-3h3M9 9H6M12 16.5h6.5M13 12.5l-2 4"/>',
'scooter':'<circle cx="6" cy="17" r="2.6"/><circle cx="18" cy="17" r="2.6"/><path d="M8.5 17H14c0-4 1-8 3-10M15 7h3M5 11h6l2 6M9 11l-1-3H5"/>',
'camera':'<path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/>',
'users':'<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0M16 4.8a3.5 3.5 0 0 1 0 6.4M18 14.5a6 6 0 0 1 3.5 5.5"/>',
'star':'<path d="M12 3l2.7 5.6 6.1.8-4.5 4.2 1.1 6.1L12 16.8 6.6 19.7l1.1-6.1L3.2 9.4l6.1-.8z"/>',
}
def sprite():
    s=''.join(f'<symbol id="i-{k}" viewBox="0 0 24 24">{v}</symbol>' for k,v in I.items())
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>{s}</defs></svg>'
def ic(name,cls=''):
    assert name in I,name
    c=('ic '+cls).strip()
    return f'<svg class="{c}" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><use href="#i-{name}"/></svg>'

FEAT=[(r'llave|keyless|smart key','key'),(r'abs','abs'),(r'freno de estacionamiento','parking'),(r'control de tracci|tcs|traction','traction'),
(r'modos de conducci|eco/sport','modes'),(r'quickshift|cambio r','bolt'),(r'puños calef|calefact','flame'),(r'bloqueo|chapa|seguridad','lock'),
(r'neum[aá]tic|presi[oó]n','tire'),(r'led|ilumin|faro|luz','light'),(r'usb|carga','usb'),(r'tft|lcd|tablero|pantalla|panel|cuadro|display|digital','screen'),
(r'bluetooth|mirroring|app','bluetooth'),(r'asiento','seat'),(r'combustible|dep[oó]sito','fuel'),(r'parabrisas|viento|visera','windshield'),
(r'guantera|ba[uú]l|maleta|topcase|parrilla|portaequipaje','box'),(r'inyecci','injection'),(r'embrague','clutch'),(r'basculante|suspensi|amortigu|horquilla|monoshock|monoamortiguador','spring'),
(r'llanta|rueda|aro','tire'),(r'freno|disco|caliper|pinza','brake'),(r'refrigera|l[ií]quido|enfria','drop'),(r'motor|cilindr|potencia','engine'),(r'tope|protec|defensa|guardabarro','shield')]
def feat_icon(t):
    t=t.lower()
    for rx,n in FEAT:
        if re.search(rx,t): return n
    return 'check'
SPEC={'Tipo de motor':'engine','Cilindrada':'piston','Relación de compresión':'gauge','Potencia máxima':'bolt','Torque máximo':'torque','Tipo de embrague':'clutch',
'Sistema de refrigeración':'drop','Sistema de alimentación':'injection','Sistema de arranque':'power','Sistema de transmisión':'gear','Transmisión final':'chain',
'Suspensión delantera':'spring','Suspensión trasera':'spring','Freno delantero':'brake','Freno trasero':'brake','Neumático delantero':'tire','Neumático trasero':'tire',
'Largo / ancho / alto (mm)':'ruler','Altura del asiento':'height','Distancia entre ejes':'wheelbase','Peso en orden de marcha':'weight','Depósito de combustible':'fuel'}
def spec_icon(label):
    if label in SPEC: return SPEC[label]
    l=label.lower()
    for k,n in (('susp','spring'),('altura','height'),('ilumin','light'),('tablero','screen'),('freno','brake')):
        if k in l: return n
    return 'check'
