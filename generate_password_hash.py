#!/usr/bin/env python3
"""
Script pour générer le hash bcrypt du nouveau mot de passe
"""
import bcrypt

password = 'MagikALi104'
hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
print("Hash bcrypt pour le mot de passe:", hashed.decode('utf-8'))
