"""Функциональный тест DeggTextJoin (Python) — без ComfyUI, без torch.

Нода склеивает подключённые тексты через разделитель. Что проверяется:
  • порядок берётся по номеру входа (text_1, text_2, …), а не по порядку
    ключей в словаре — иначе склейка зависела бы от того, как ComfyUI
    собрал kwargs;
  • пустой вход ("") и None пропускаются, иначе в промпте появляются
    двойные разделители (самая частая жалоба «запятая запятой»);
  • нет ни одного текста → пустая строка, а не падение;
  • разделитель уважается буквально (в том числе "\\n" и ""), текст не
    обрезается и не нормализуется;
  • потолок 20 из DESCRIPTION: text_21 не участвует.

Запуск:  cd Degg_TextJoin && python tests/_test_deg_text_join.py
"""

import importlib.util
import sys
from pathlib import Path

NODE = Path(__file__).resolve().parent.parent / "deg_text_join_node.py"

fails = []
oks = []


def _p(text):
    try:
        enc = sys.stdout.encoding or "utf-8"
        sys.stdout.write(str(text).encode(enc, "replace").decode(enc, "replace") + "\n")
    except Exception:
        pass


def check(name, cond, extra=""):
    (oks if cond else fails).append(name)
    _p(("  ok  " if cond else "  FAIL") + f"  {name}" + (f"  [{extra}]" if extra and not cond else ""))


spec = importlib.util.spec_from_file_location("deg_text_join_node", NODE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

Cls = mod.NODE_CLASS_MAPPINGS["DeggTextJoin"]
it = Cls.INPUT_TYPES()
node = Cls()

# ────────────────────────────── контракт входа ──────────────────────────────
check("INPUT_TYPES: separator — STRING с default \", \"",
      it["required"]["separator"][0] == "STRING"
      and it["required"]["separator"][1].get("default") == ", ",
      it["required"]["separator"])
check("INPUT_TYPES: первый текст — optional text_1 с forceInput",
      list(it.get("optional", {})) == ["text_1"]
      and it["optional"]["text_1"][1].get("forceInput") is True,
      it.get("optional"))

# ──────────────────────────────── склейка ───────────────────────────────────
check("join: два текста через \", \"", node.join(", ", text_1="мама", text_2="мыла") == ("мама, мыла",),
      node.join(", ", text_1="мама", text_2="мыла"))
check("join: порядок по номеру входа, а не по порядку kwargs",
      node.join(" | ", text_3="три", text_1="один") == ("один | три",),
      node.join(" | ", text_3="три", text_1="один"))
check("join: пустой вход пропускается (нет двойного разделителя)",
      node.join(", ", text_1="мама", text_2="", text_3="раму") == ("мама, раму",),
      node.join(", ", text_1="мама", text_2="", text_3="раму"))
check("join: None пропускается",
      node.join(", ", text_1="мама", text_2=None, text_3="раму") == ("мама, раму",))
check("join: нет ни одного текста → пустая строка", node.join(", ") == ("",), node.join(", "))
check("join: все входы пустые → пустая строка",
      node.join(", ", text_1="", text_2="") == ("",))
check("join: разделитель \"\\n\" идёт буквально",
      node.join("\n", text_1="а", text_2="б") == ("а\nб",), node.join("\n", text_1="а", text_2="б"))
check("join: пустой разделитель склеивает без вставок",
      node.join("", text_1="а", text_2="б") == ("аб",), node.join("", text_1="а", text_2="б"))
check("join: текст не обрезается (пробелы значимы)",
      node.join("|", text_1=" а ", text_2="б") == (" а |б",),
      node.join("|", text_1=" а ", text_2="б"))
check("join: потолок 20 из описания — text_21 не участвует",
      node.join(", ", text_20="двадцать", text_21="двадцать один") == ("двадцать",),
      node.join(", ", text_20="двадцать", text_21="двадцать один"))
check("join: 20 текстов склеиваются все",
      node.join("-", **{f"text_{i}": str(i) for i in range(1, 21)})
      == ("-".join(str(i) for i in range(1, 21)),))
check("join: многострочный текст сохраняет переводы строк",
      node.join(" ", text_1="a\nb", text_2="c") == ("a\nb c",),
      repr(node.join(" ", text_1="a\nb", text_2="c")))

# ─────────────────────────── метаданные класса/меню ────────────────────────
check("RETURN_TYPES = (STRING,)", Cls.RETURN_TYPES == ("STRING",), Cls.RETURN_TYPES)
check("RETURN_NAMES = (text,)", Cls.RETURN_NAMES == ("text",), Cls.RETURN_NAMES)
check("FUNCTION = join", Cls.FUNCTION == "join", Cls.FUNCTION)
check("REGISTRY-ключ не переименован", mod.NODE_CLASS_MAPPINGS == {"DeggTextJoin": Cls},
      list(mod.NODE_CLASS_MAPPINGS))
check("имя в меню на месте",
      mod.NODE_DISPLAY_NAME_MAPPINGS.get("DeggTextJoin") == "Degg Text Join",
      mod.NODE_DISPLAY_NAME_MAPPINGS)

_p("")
_p(f"PASS: {len(oks)}  FAIL: {len(fails)}")
if fails:
    _p("failed: " + ", ".join(fails))
else:
    _p("ТЕСТ ПРОЙДЕН")
sys.exit(1 if fails else 0)
