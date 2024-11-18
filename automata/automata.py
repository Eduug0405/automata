class Automata:
    def __init__(self):
        self.estado_actual = 'q0'
        self.estados_aceptacion = {'q5','q30'}  # Estados finales por definir
        self.transition = {

            "q0": {"Q": "q1", "F": "q1",
                   "S": "q8", "D": "q12",
                   "q": "q24"},
            "q1": {" ": "q1", "=":"q2"},
            "q2": {" ": "q2", "{":"q3"},
            "q3": {" ": "q3", "q": "q6",
                   **{chr(i): "q4" for i in range(ord('A'), ord('Z') + 1)},
                   **{chr(i): "q4" for i in range(ord('0'), ord('9') + 1)}
                   },
            "q4": {" ": "q4", "}": "q5",",":"q3",
                   **{chr(i): "q4" for i in range(ord('0'), ord('9') + 1)}
                   },
            "q6": {
                **{chr(i): "q7" for i in range(ord('0'), ord('9') + 1)}
            },
            "q7":{",":"q3","}":"q5",
                **{chr(i): "q7" for i in range(ord('0'), ord('9') + 1)}
            },
            "q8":{
                " ":"q8", "=":"q9"
            },
            "q9":{
                " ":"q9", "{":"q10",
            },
            "q10":{
                " ":"q10",
                **{chr(i): "q11" for i in range(ord('a'), ord('z') + 1)},
                **{chr(i): "q11" for i in range(ord('0'), ord('9') + 1)}
            },
            "q11":{
              ",":"q10","}":"q5"," ":"q11",
            },
            "q12":{
                " ":"q12", "=":"q13",
            },
            "q13":{
                " ":"q13", "{":"q14",
            },
            "q14":{
                " ":"q14", "(":"q15",
            },
            "q15":{
                "q":"q22"," ":"q15",
                **{chr(i): "q16" for i in range(ord('A'), ord('Z') + 1)},
                **{chr(i): "q16" for i in range(ord('0'), ord('9') + 1)}
            },
            "q16":{
                **{chr(i): "q16" for i in range(ord('0'), ord('9') + 1)}, ",":"q17", " ":"q16",
            },
            "q17":{
                " ": "q17",
                **{chr(i): "q18" for i in range(ord('a'), ord('z') + 1)},
                **{chr(i): "q18" for i in range(ord('0'), ord('9') + 1)}
            },
            "q18":{
              ",":"q19", " ":"q18",
            },
            "q19":{
                "q":"q23"," ":"q19",
                **{chr(i): "q20" for i in range(ord('A'), ord('Z') + 1)},
                **{chr(i): "q20" for i in range(ord('0'), ord('9') + 1)}
            },
            "q20":{
                **{chr(i): "q20" for i in range(ord('0'), ord('9') + 1)},
                ")":"q21", " ":"q20",
            },
            "q21":{
                "}":"q5",",":"q14"," ":"q21",
            },
            "q22":{
                **{chr(i): "q16" for i in range(ord('0'), ord('9') + 1)}
            },
            "q23":{
                **{chr(i): "q20" for i in range(ord('0'), ord('9') + 1)}
            },
            "q24":{
                "0":"q25"
            },
            "q25":{
                " ":"q25", "=":"q26",
            },
            "q26":{
                "{":"q27","q":"q29","A":"q30"," ":"q26"
            },
            "q27":{
                "0":"q28"
            },
            "q28":{
                "}":"q5"
            },
            "q29":{
                "0":"q30"
            }

        }

    def extraer_patrones(self, texto):
        patrones = []
        buffer = ''
        self.estado_actual = 'q0'

        for char in texto:
            if char in self.transition[self.estado_actual]:
                buffer += char
                self.estado_actual = self.transition[self.estado_actual][char]
                if self.estado_actual in self.estados_aceptacion:
                    patrones.append(buffer)
                    buffer = ''
                    self.estado_actual = 'q0'
            else:
                buffer = ''
                self.estado_actual = 'q0'

        return patrones

