from outils import *


class InputTextBox:
    def __init__(self, title):
        self.enable = True
        self.title = title

        self.l = 350
        self.h = 50
        self.x = int((LARGEUR - self.l) / 2)
        self.y = int((HAUTEUR - self.h) / 2 + 100)
        
        self.m = 5
        self.msg = ''
        SCREEN.blit(IMAGE_VOLEUR, (20, 20))
        self.font = pygame.font.Font(POLICE_NONE, int((self.h * 2 - 7 * self.m) / COEF_POLICE))
        self.ts = self.font.render(self.msg, True, NOIR)
        self.b = Bouton(self.x, self.y + self.h + 15, '', self.l, self.h, texte='Valider', tailleTexte=50)
        self.etape = 0
        self.reessayer = False

    def clic(self, x_souris, y_souris):
        if self.x < x_souris < self.x + self.l and self.y < y_souris < self.y + self.h:
            self.enable = True
        else:
            if self.b.clic(x_souris, y_souris):
                if self.msg != '':
                    return self.msg
            self.enable = False
        return None
    
    def input_text(self, event):
        if self.enable:
            if event.key == pygame.K_RETURN or event.key == 271:
                if self.msg != '':
                    return self.msg
            elif event.key == pygame.K_BACKSPACE:
                self.msg = self.msg[:-1]
            else:
                self.msg += event.unicode
            self.ts = self.font.render(self.msg, True, NOIR)
        return None

    def display(self):
        affiche_texte(self.title, LARGEUR / 2 - MARGES, HAUTEUR_TITRE / 2 + 50, None, 52, GRIS_FONCE, centrer=True)
        rectangle(MARGES, 2 * MARGES + HAUTEUR_TITRE, LARGEUR - 2 * MARGES, HAUTEUR - 3 * MARGES - HAUTEUR_TITRE)
        c = GRIS_CLAIR
        if self.enable:
            c = GRIS_FONCE
        pygame.draw.rect(SCREEN, c, (self.x, self.y, self.l, self.h), 3)
        SCREEN.blit(self.ts, (int(self.x + self.l / 2 - self.ts.get_width() / 2), self.y + self.m))
        cusor_x = (int(self.x + self.l / 2 - self.ts.get_width() / 2) + self.ts.get_width(), self.y + self.m+ self.ts.get_height())
        # cursor
        if self.enable and time.time() % 1 < 0.5:
            pygame.draw.line(SCREEN, NOIR, cusor_x,
                                (cusor_x[0], cusor_x[1] - self.ts.get_height()), 2)
        self.b.affiche()
        self.display_icon()
    
    def display_icon(self):
        pass