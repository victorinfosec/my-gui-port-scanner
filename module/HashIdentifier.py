import hashid

def identify_hash(hash_input, result_textbox):
    """Identifie les 3 types de hash les plus plausibles et affiche les résultats."""
    if not hash_input.strip():
        result_textbox.configure(state="normal")
        result_textbox.delete("1.0", "end")
        result_textbox.insert("1.0", "Veuillez entrer un hash valide.\n")
        result_textbox.configure(state="disabled")
        return

    try:
        # Créer une instance de HashID et identifier le hash
        hashid_instance = hashid.HashID()
        matches = hashid_instance.identifyHash(hash_input)

        result_textbox.configure(state="normal")
        result_textbox.delete("1.0", "end")

        if matches:
            # Trier les résultats par popularité (Hashcat ID, John ID, ou nom comme fallback)
            sorted_matches = sorted(
                matches, 
                key=lambda match: (match.hashcat is not None, match.john is not None, match.name),
                reverse=True
            )

            # Garder seulement les 3 premiers
            top_matches = sorted_matches[:3]

            # Préparer les résultats pour l'affichage
            results = "Les 3 types de hash les plus plausibles :\n"
            for match in top_matches:
                name = match.name
                hashcat = match.hashcat if match.hashcat else "N/A"
                john = match.john if match.john else "N/A"
                results += f"- {name} (Hashcat ID: {hashcat}, John ID: {john})\n"

            result_textbox.insert("1.0", results)
        else:
            result_textbox.insert("1.0", "Aucun type de hash identifié.\n")

        result_textbox.configure(state="disabled")
    except Exception as e:
        result_textbox.configure(state="normal")
        result_textbox.delete("1.0", "end")
        result_textbox.insert("1.0", f"Erreur lors de l'identification : {str(e)}\n")
        result_textbox.configure(state="disabled")
