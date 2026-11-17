<?php
// Recibe el formulario de cotización/contacto y lo envía por correo.
// Funciona en cualquier cPanel con PHP 7.4+ sin configuración extra.
// Para cambiar el destinatario, edita solo la línea $DESTINO.
$DESTINO = 'contacto@imoto.cl';

header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store');

function out($ok, $msg, $code = 200) {
    http_response_code($code);
    echo json_encode(['ok' => $ok, 'msg' => $msg], JSON_UNESCAPED_UNICODE);
    exit;
}
function limpia($s, $max) {
    $s = trim((string)$s);
    $s = preg_replace('/[\x00-\x08\x0B\x0C\x0E-\x1F]/', '', $s);
    return mb_substr($s, 0, $max);
}
function una_linea($s) { return trim(preg_replace('/\s+/', ' ', $s)); } // evita inyección de cabeceras

if ($_SERVER['REQUEST_METHOD'] !== 'POST') out(false, 'Método no permitido.', 405);

// Campo trampa: los humanos no lo ven; los bots sí lo llenan. Se responde "ok" sin enviar nada.
if (!empty($_POST['sitio'])) out(true, 'Solicitud enviada.');

// Límite simple: 5 envíos por IP cada 10 minutos.
$ip = $_SERVER['REMOTE_ADDR'] ?? '0';
$f = sys_get_temp_dir() . '/zontes_rl_' . md5($ip);
$ahora = time();
$marcas = [];
if (is_file($f)) $marcas = array_filter(array_map('intval', explode(',', (string)@file_get_contents($f))), function ($t) use ($ahora) { return $t > $ahora - 600; });
if (count($marcas) >= 5) out(false, 'Demasiados envíos seguidos. Inténtalo en unos minutos.', 429);

$nombre   = una_linea(limpia($_POST['nombre'] ?? '', 100));
$correo   = una_linea(limpia($_POST['correo'] ?? '', 150));
$telefono = una_linea(limpia($_POST['telefono'] ?? '', 40));
$region   = una_linea(limpia($_POST['region'] ?? '', 80));
$modelo   = una_linea(limpia($_POST['modelo_nombre'] ?? '', 80));
$mensaje  = limpia($_POST['mensaje'] ?? '', 2000);

if ($nombre === '' || $telefono === '' || $region === '' || $modelo === '' || !filter_var($correo, FILTER_VALIDATE_EMAIL)) {
    out(false, 'Revisa los campos del formulario.', 422);
}

$host = preg_replace('/^www\./', '', $_SERVER['HTTP_HOST'] ?? 'localhost');
$host = preg_replace('/:\d+$/', '', $host);
$remitente = 'no-responder@' . $host;

$asunto = '=?UTF-8?B?' . base64_encode('Cotización ' . $modelo . ' — sitio Zontes Chile') . '?=';
$cuerpo = "Nueva solicitud de cotización desde el sitio web\r\n\r\n"
        . "Modelo: $modelo\r\nNombre: $nombre\r\nCorreo: $correo\r\nTeléfono: $telefono\r\nRegión: $region\r\n\r\n"
        . ($mensaje !== '' ? "Mensaje:\r\n$mensaje\r\n" : "Sin mensaje adicional.\r\n");
$cab = "From: Sitio Zontes Chile <$remitente>\r\n"
     . "Reply-To: $nombre <$correo>\r\n"
     . "MIME-Version: 1.0\r\nContent-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: 8bit\r\n"
     . "X-Mailer: PHP/" . phpversion() . "\r\n";

$enviado = @mail($DESTINO, $asunto, $cuerpo, $cab, '-f' . $remitente);
if (!$enviado) $enviado = @mail($DESTINO, $asunto, $cuerpo, $cab); // algunos hosting rechazan -f

if (!$enviado) {
    error_log('zontes enviar.php: mail() falló para ' . $correo);
    out(false, 'No pudimos enviar tu solicitud. Escríbenos a ' . $DESTINO . '.', 500);
}

$marcas[] = $ahora;
@file_put_contents($f, implode(',', $marcas));
out(true, 'Solicitud enviada. Te contactaremos pronto.');
