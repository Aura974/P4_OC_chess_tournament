from utils.utils import (is_date_valid, error_message,
                         is_elo_valid, is_gender_valid, is_player_name_valid, is_query_empty, print_text)
from view.player_view import (existing_player_choice, get_player_birthday,
                              get_player_elo, get_player_gender,
                              get_player_name, get_player_surname,
                              players_choice, get_existing_player,
                              print_players_title, get_new_elo,
                              print_existing_players)
from model.player import Player
from tinydb import TinyDB, Query
from controller.serializer_controller import (player_list_serializer,
                                              player_list_deserializer)
import os


class PlayerController:
    def __init__(self):
        self.player = None
        self.db = TinyDB("players_data.json", indent=4)
        self.players_data = self.db.table("players_data")

    def new_player(self):
        players = Query()
        name, surname = self.get_and_check_name()
        elo = self.get_and_check_elo()
        self.player = Player(name, surname, elo, score=0)
        db_players = self.players_data.search((players.name == name) &
                                              (players.surname == surname) &
                                              (players.elo == elo))

        while not is_query_empty(db_players):
            error_message("Joueur déjà dans la base de données")
            name, surname = self.get_and_check_name()
            elo = self.get_and_check_elo()
            db_players = self.players_data.search((players.name == name) &
                                                  (players.surname == surname) &
                                                  (players.elo == elo))

        self.player = Player(name, surname, elo, score=0)
        self.player.birthday = self.get_and_check_date()
        self.player.gender = self.get_and_check_gender()
        self.players_data.insert(player_list_serializer(self.player))

        return self.player

    def reload_player(self):
        self.db = TinyDB("players_data.json", indent=4)
        players = Query()
        self.player_data = self.db.table('players_data')

        existing_player = get_existing_player()

        db_player = self.player_data.search(players.name == existing_player)

        while is_query_empty(db_player):
            error_message("Aucune donnée pour ce joueur.")
            existing_player = get_existing_player()
            db_player = self.players_data.search(players.name == existing_player)

        for db_play in db_player:
            print_existing_players(db_play)

        choice = existing_player_choice()

        reloaded_player = self.player_data.get(doc_id=choice)

        self.player = None
        self.player = player_list_deserializer(reloaded_player)
        return self.player

    def handle_players_choice(self):
        choice = players_choice()
        while (choice != "1" and choice != "2"):
            error_message("Choisissez 1 ou 2 uniquement")
            choice = players_choice()
        else:
            if (choice == "1"):
                choice = self.new_player()
            elif (choice == "2"):
                choice = self.reload_player()
        return choice

    def get_and_check_name(self):
        name = get_player_name()
        name = name.strip().title()
        while not is_player_name_valid(name):
            error_message("Le format du prénom est incorrect")
            name = get_player_name()
            name = name.strip().title()
        else:
            surname = get_player_surname()
            surname = surname.strip().upper()
            while not is_player_name_valid(surname):
                error_message("Le format du nom est incorrect")
                surname = get_player_surname()
                surname = surname.strip().upper()
        return name, surname

    def get_and_check_elo(self):
        elo = get_player_elo()
        while not is_elo_valid(elo):
            error_message("Veuillez entrer un nombre")
            elo = get_player_elo()
        return int(elo)

    def get_and_check_date(self):
        birthday = get_player_birthday()
        while not is_date_valid(birthday):
            error_message("La date n'a pas le bon format dd/mm/YYYY")
            birthday = get_player_birthday()
        return birthday

    def get_and_check_gender(self):
        gender = get_player_gender()
        gender = gender.lower()
        while not is_gender_valid(gender):
            error_message("Veuillez entrer uniquement 'f' ou 'm'")
            gender = get_player_gender()
            gender.lower()
        return gender.upper()

    def update_player_elo():
        db = TinyDB("players_data.json", indent=4)
        players = Query()
        player_data = db.table('players_data')

        existing_player = get_existing_player()

        db_players = player_data.search(players.name == existing_player)

        while is_query_empty(db_players):
            error_message("Aucun joueur trouvé")
            existing_player = get_existing_player()
            db_players = player_data.search(players.name == existing_player)

        print_players_title()
        for db_play in db_players:
            print_existing_players(db_play)

        choice = existing_player_choice()

        new_elo = get_new_elo()

        while not is_elo_valid(new_elo):
            error_message("Veuillez entrer un nombre")
            new_elo = get_new_elo()
        else:
            new_elo = int(new_elo)
            os.system("cls")
            print_text("Changement validé !")
            player_data.update({"elo": new_elo}, doc_ids=[choice])
            uploaded_player = player_data.get(doc_id=choice)
            print_existing_players(uploaded_player)

        return new_elo
