# PPT_Ai_WEB
Crea presentaciones desde LLM, PDF y WEB

### Sobre la Validación de Credenciales

En cuanto a la validación de credenciales del usuario, Flask-Security maneja este proceso internamente cuando el usuario intenta iniciar sesión. Cuando el usuario envía el formulario de inicio de sesión, Flask-Security recoge las credenciales ingresadas, las valida contra la base de datos, y maneja la creación de la sesión del usuario si las credenciales son correctas.

Si quieres personalizar el proceso de autenticación o realizar acciones adicionales durante la autenticación, podrías necesitar explorar los [signals](https://flask-security-too.readthedocs.io/en/stable/signals.html) de Flask-Security o sobrescribir las [vistas](https://flask-security-too.readthedocs.io/en/stable/customizing.html) predeterminadas.
