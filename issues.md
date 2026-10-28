# Static Code Analysis — Issue Log

> Issue locations below refer to the original `flight_reservation_system.py`. Run the tools locally and update the lines/codes to match the actual reports produced by your environment.

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Unsafe `eval()` | Security / High | 47 | `eval(surcharge_expr)` evaluates arbitrary Python expressions, which could execute unwanted code. | Replaced the expression string with a numeric `surcharge_rate`, validated that it is between 0 and 1, and performed arithmetic directly. |
| Hardcoded API secret | Security / High | 69 | A credential is embedded in source code and printed to the terminal, where it could be exposed. | Removed the hardcoded token and its print statement. Secrets should be supplied through protected configuration/environment variables if needed. |
| Shell command injection risk | Security / Medium | 61 | Passing a filename into `os.system()` allows shell interpretation of user-controlled characters. | Removed the shell call and used a normal Python status message. |
| Mutable default argument | Correctness / Medium | 15 | `baggage_tags=[]` is shared between calls and can retain data from earlier bookings. | Changed the default to `None` and initialized a new list inside the function. |
| Broad exception swallowed | Reliability / Medium | 29–33 | Bare `except:` hides all errors and makes an invalid flight indistinguishable from a successful cancellation. | Used dictionary lookup to handle an unknown flight explicitly and return `False`. |
| Weak hashing algorithm | Security | 66 | MD5 is unsuitable where a modern cryptographic digest is expected. | Changed the sample digest to SHA-256. For password storage, use a dedicated password-hashing algorithm instead. |
| Non-cryptographic PIN generator | Security | 71 | `random.randint()` is not intended for security-sensitive tokens. | Used `secrets.randbelow()` to generate the PIN. |
| Unused imports and variables | Code quality | 4, 5, 34, 55 | `math`, the `airport_fee` variable, and a loop variable are unused. | Removed unused code and simplified the summary calculation. |
| Naming, formatting, and file handling | Style / Maintainability | Multiple | CamelCase names, `%` formatting, manual file open/close, and no main guard reduce readability or robustness. | Used snake_case names, f-strings, `Path.write_text()`, a module docstring, and `if __name__ == "__main__":`. |
