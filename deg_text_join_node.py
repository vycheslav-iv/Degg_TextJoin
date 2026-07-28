class DeggTextJoin:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "separator": ("STRING", {
                    "default": ", ",
                    "multiline": False,
                    "tooltip": "Разделитель между текстами (например: ', ', '\\n', ' ' — пробел)",
                }),
            },
            "optional": {
                "text_1": ("STRING", {
                    "forceInput": True,
                    "multiline": True,
                    "tooltip": "Текст для объединения",
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "join"
    CATEGORY = "My_custom_nodes"
    DESCRIPTION = (
        "Объединяет несколько текстов через разделитель. "
        "При подключении к text_N появляется text_{N+1}. "
        "Максимум 20 текстов."
    )

    def join(self, separator, **kwargs):
        texts = []
        for i in range(1, 21):
            key = f"text_{i}"
            val = kwargs.get(key)
            if val is not None and val != "":
                texts.append(val)
        result = separator.join(texts)
        return (result,)


NODE_CLASS_MAPPINGS = {
    "DeggTextJoin": DeggTextJoin,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "DeggTextJoin": "Degg Text Join",
}
