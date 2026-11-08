import sys
import os

path = os.path.join(os.environ['HOME'], 'mnt', 'pocketsage', 'index.html')
content = open(path, encoding='utf-8').read()

TRANSLATIONS_JS = r"""
// ══════════════════════════════════════════════════════════════
// TRANSLATIONS — Traductions UI selon langue maternelle
// ══════════════════════════════════════════════════════════════
const TRANSLATIONS = {
  FR: {
    start:'▶ Commencer !', play:'▶ Jouer !', validate:'✅ Valider',
    next:'Suivant →', back:'← Retour', close:'Fermer', cancel:'Annuler',
    correct:'Bravo !', wrong:'Essaie encore !', score:'Score',
    home:'🏠 Accueil', profile:'Profil', settings:'Réglages',
    done:'Séance terminée !', retry:'Recommencer', listen:'🔊 Écouter',
    hint:'💡 Indice', question:'Question', answer:'Réponse',
    success:'Excellent !', create_profile:'✨ Créer mon profil !',
    add_profile:'➕ Ajouter un profil', firstname:'👤 Prénom',
    native_lang:'🗺️ Langue maternelle', learning_lang:'🌍 Langues à apprendre',
    age:'🎂 Ton âge', avatar:'🎭 Choisis ton avatar',
    confirm_pin:'Confirmer PIN', new_pin:'Nouveau PIN',
    export:'💾 Exporter', report:'📊 Bilan', stop:'⏹ Arrêter',
    challenge:'Défi suivant →', well_done:'Bien joué !',
    understood:'Compris ✓', placeholder_name:'Emma, Lucas, Maman…',
    send_feedback:'Envoyer', feedback_placeholder:'Vos remarques, idées…',
  },
  EN: {
    start:'▶ Start!', play:'▶ Play!', validate:'✅ Validate',
    next:'Next →', back:'← Back', close:'Close', cancel:'Cancel',
    correct:'Well done!', wrong:'Try again!', score:'Score',
    home:'🏠 Home', profile:'Profile', settings:'Settings',
    done:'Session complete!', retry:'Retry', listen:'🔊 Listen',
    hint:'💡 Hint', question:'Question', answer:'Answer',
    success:'Excellent!', create_profile:'✨ Create my profile!',
    add_profile:'➕ Add a profile', firstname:'👤 First name',
    native_lang:'🗺️ Native language', learning_lang:'🌍 Languages to learn',
    age:'🎂 Your age', avatar:'🎭 Choose your avatar',
    confirm_pin:'Confirm PIN', new_pin:'New PIN',
    export:'💾 Export', report:'📊 Report', stop:'⏹ Stop',
    challenge:'Next challenge →', well_done:'Well done!',
    understood:'Got it ✓', placeholder_name:'Emma, Lucas, Mum…',
    send_feedback:'Send', feedback_placeholder:'Your comments, ideas…',
  },
  DE: {
    start:'▶ Starten!', play:'▶ Spielen!', validate:'✅ Bestätigen',
    next:'Weiter →', back:'← Zurück', close:'Schließen', cancel:'Abbrechen',
    correct:'Super!', wrong:'Versuch es nochmal!', score:'Punktzahl',
    home:'🏠 Startseite', profile:'Profil', settings:'Einstellungen',
    done:'Sitzung beendet!', retry:'Nochmal', listen:'🔊 Anhören',
    hint:'💡 Hinweis', question:'Frage', answer:'Antwort',
    success:'Ausgezeichnet!', create_profile:'✨ Mein Profil erstellen!',
    add_profile:'➕ Profil hinzufügen', firstname:'👤 Vorname',
    native_lang:'🗺️ Muttersprache', learning_lang:'🌍 Sprachen lernen',
    age:'🎂 Dein Alter', avatar:'🎭 Avatar wählen',
    confirm_pin:'PIN bestätigen', new_pin:'Neue PIN',
    export:'💾 Exportieren', report:'📊 Bericht', stop:'⏹ Stopp',
    challenge:'Nächste Herausforderung →', well_done:'Gut gemacht!',
    understood:'Verstanden ✓', placeholder_name:'Emma, Lucas, Mama…',
    send_feedback:'Senden', feedback_placeholder:'Ihre Kommentare, Ideen…',
  },
  ES: {
    start:'▶ ¡Empezar!', play:'▶ ¡Jugar!', validate:'✅ Validar',
    next:'Siguiente →', back:'← Volver', close:'Cerrar', cancel:'Cancelar',
    correct:'¡Bravo!', wrong:'¡Inténtalo de nuevo!', score:'Puntuación',
    home:'🏠 Inicio', profile:'Perfil', settings:'Ajustes',
    done:'¡Sesión terminada!', retry:'Reintentar', listen:'🔊 Escuchar',
    hint:'💡 Pista', question:'Pregunta', answer:'Respuesta',
    success:'¡Excelente!', create_profile:'✨ ¡Crear mi perfil!',
    add_profile:'➕ Añadir perfil', firstname:'👤 Nombre',
    native_lang:'🗺️ Lengua materna', learning_lang:'🌍 Idiomas a aprender',
    age:'🎂 Tu edad', avatar:'🎭 Elige tu avatar',
    confirm_pin:'Confirmar PIN', new_pin:'Nuevo PIN',
    export:'💾 Exportar', report:'📊 Informe', stop:'⏹ Parar',
    challenge:'Siguiente reto →', well_done:'¡Bien hecho!',
    understood:'Entendido ✓', placeholder_name:'Emma, Lucas, Mamá…',
    send_feedback:'Enviar', feedback_placeholder:'Tus comentarios, ideas…',
  },
  IT: {
    start:'▶ Inizia!', play:'▶ Gioca!', validate:'✅ Conferma',
    next:'Avanti →', back:'← Indietro', close:'Chiudi', cancel:'Annulla',
    correct:'Bravo!', wrong:'Riprova!', score:'Punteggio',
    home:'🏠 Home', profile:'Profilo', settings:'Impostazioni',
    done:'Sessione terminata!', retry:'Riprova', listen:'🔊 Ascolta',
    hint:'💡 Suggerimento', question:'Domanda', answer:'Risposta',
    success:'Eccellente!', create_profile:'✨ Crea il mio profilo!',
    add_profile:'➕ Aggiungi profilo', firstname:'👤 Nome',
    native_lang:'🗺️ Lingua madre', learning_lang:'🌍 Lingue da imparare',
    age:'🎂 La tua età', avatar:'🎭 Scegli il tuo avatar',
    confirm_pin:'Conferma PIN', new_pin:'Nuovo PIN',
    export:'💾 Esporta', report:'📊 Rapporto', stop:'⏹ Stop',
    challenge:'Prossima sfida →', well_done:'Ben fatto!',
    understood:'Capito ✓', placeholder_name:'Emma, Lucas, Mamma…',
    send_feedback:'Invia', feedback_placeholder:'Commenti, idee…',
  },
  PT: {
    start:'▶ Começar!', play:'▶ Jogar!', validate:'✅ Validar',
    next:'Próximo →', back:'← Voltar', close:'Fechar', cancel:'Cancelar',
    correct:'Parabéns!', wrong:'Tente novamente!', score:'Pontuação',
    home:'🏠 Início', profile:'Perfil', settings:'Configurações',
    done:'Sessão concluída!', retry:'Tentar novamente', listen:'🔊 Ouvir',
    hint:'💡 Dica', question:'Pergunta', answer:'Resposta',
    success:'Excelente!', create_profile:'✨ Criar meu perfil!',
    add_profile:'➕ Adicionar perfil', firstname:'👤 Nome',
    native_lang:'🗺️ Língua materna', learning_lang:'🌍 Idiomas a aprender',
    age:'🎂 Sua idade', avatar:'🎭 Escolha seu avatar',
    confirm_pin:'Confirmar PIN', new_pin:'Novo PIN',
    export:'💾 Exportar', report:'📊 Relatório', stop:'⏹ Parar',
    challenge:'Próximo desafio →', well_done:'Muito bem!',
    understood:'Entendido ✓', placeholder_name:'Emma, Lucas, Mamãe…',
    send_feedback:'Enviar', feedback_placeholder:'Seus comentários, ideias…',
  },
  RU: {
    start:'▶ Начать!', play:'▶ Играть!', validate:'✅ Подтвердить',
    next:'Далее →', back:'← Назад', close:'Закрыть', cancel:'Отмена',
    correct:'Молодец!', wrong:'Попробуй ещё!', score:'Очки',
    home:'🏠 Главная', profile:'Профиль', settings:'Настройки',
    done:'Занятие завершено!', retry:'Повторить', listen:'🔊 Слушать',
    hint:'💡 Подсказка', question:'Вопрос', answer:'Ответ',
    success:'Отлично!', create_profile:'✨ Создать профиль!',
    add_profile:'➕ Добавить профиль', firstname:'👤 Имя',
    native_lang:'🗺️ Родной язык', learning_lang:'🌍 Изучаемые языки',
    age:'🎂 Твой возраст', avatar:'🎭 Выбери аватар',
    confirm_pin:'Подтвердить PIN', new_pin:'Новый PIN',
    export:'💾 Экспорт', report:'📊 Отчёт', stop:'⏹ Стоп',
    challenge:'Следующее задание →', well_done:'Хорошая работа!',
    understood:'Понял ✓', placeholder_name:'Эмма, Лукас, Мама…',
    send_feedback:'Отправить', feedback_placeholder:'Ваши комментарии, идеи…',
  },
  UK: {
    start:'▶ Почати!', play:'▶ Грати!', validate:'✅ Підтвердити',
    next:'Далі →', back:'← Назад', close:'Закрити', cancel:'Скасувати',
    correct:'Молодець!', wrong:'Спробуй ще!', score:'Очки',
    home:'🏠 Головна', profile:'Профіль', settings:'Налаштування',
    done:'Заняття завершено!', retry:'Повторити', listen:'🔊 Слухати',
    hint:'💡 Підказка', question:'Питання', answer:'Відповідь',
    success:'Чудово!', create_profile:'✨ Створити профіль!',
    add_profile:'➕ Додати профіль', firstname:"👤 Ім'я",
    native_lang:'🗺️ Рідна мова', learning_lang:'🌍 Мови для вивчення',
    age:'🎂 Твій вік', avatar:'🎭 Обери аватар',
    confirm_pin:'Підтвердити PIN', new_pin:'Новий PIN',
    export:'💾 Експорт', report:'📊 Звіт', stop:'⏹ Стоп',
    challenge:'Наступне завдання →', well_done:'Гарна робота!',
    understood:'Зрозумів ✓', placeholder_name:'Емма, Лукас, Мама…',
    send_feedback:'Надіслати', feedback_placeholder:'Коментарі, ідеї…',
  },
  AR: {
    start:'▶ ابدأ!', play:'▶ العب!', validate:'✅ تأكيد',
    next:'التالي →', back:'← رجوع', close:'إغلاق', cancel:'إلغاء',
    correct:'أحسنت!', wrong:'حاول مرة أخرى!', score:'النقاط',
    home:'🏠 الرئيسية', profile:'الملف الشخصي', settings:'الإعدادات',
    done:'انتهت الجلسة!', retry:'إعادة المحاولة', listen:'🔊 استمع',
    hint:'💡 تلميح', question:'سؤال', answer:'إجابة',
    success:'ممتاز!', create_profile:'✨ إنشاء ملفي الشخصي!',
    add_profile:'➕ إضافة ملف', firstname:'👤 الاسم',
    native_lang:'🗺️ اللغة الأم', learning_lang:'🌍 اللغات للتعلم',
    age:'🎂 عمرك', avatar:'🎭 اختر صورتك',
    confirm_pin:'تأكيد الرمز', new_pin:'رمز جديد',
    export:'💾 تصدير', report:'📊 تقرير', stop:'⏹ إيقاف',
    challenge:'التحدي التالي →', well_done:'عمل رائع!',
    understood:'فهمت ✓', placeholder_name:'إيما، لوكاس، ماما…',
    send_feedback:'إرسال', feedback_placeholder:'تعليقاتك، أفكارك…',
  },
  ZH: {
    start:'▶ 开始！', play:'▶ 玩！', validate:'✅ 确认',
    next:'下一步 →', back:'← 返回', close:'关闭', cancel:'取消',
    correct:'太棒了！', wrong:'再试一次！', score:'分数',
    home:'🏠 主页', profile:'个人资料', settings:'设置',
    done:'课程结束！', retry:'重试', listen:'🔊 听',
    hint:'💡 提示', question:'问题', answer:'答案',
    success:'优秀！', create_profile:'✨ 创建我的资料！',
    add_profile:'➕ 添加资料', firstname:'👤 名字',
    native_lang:'🗺️ 母语', learning_lang:'🌍 要学的语言',
    age:'🎂 你的年龄', avatar:'🎭 选择头像',
    confirm_pin:'确认PIN', new_pin:'新PIN',
    export:'💾 导出', report:'📊 报告', stop:'⏹ 停止',
    challenge:'下一个挑战 →', well_done:'干得好！',
    understood:'明白了 ✓', placeholder_name:'艾玛、卢卡斯、妈妈…',
    send_feedback:'发送', feedback_placeholder:'您的意见、想法…',
  },
  PL: {
    start:'▶ Zacznij!', play:'▶ Graj!', validate:'✅ Potwierdź',
    next:'Dalej →', back:'← Wstecz', close:'Zamknij', cancel:'Anuluj',
    correct:'Brawo!', wrong:'Spróbuj ponownie!', score:'Wynik',
    home:'🏠 Strona główna', profile:'Profil', settings:'Ustawienia',
    done:'Sesja zakończona!', retry:'Ponów', listen:'🔊 Słuchaj',
    hint:'💡 Podpowiedź', question:'Pytanie', answer:'Odpowiedź',
    success:'Doskonale!', create_profile:'✨ Utwórz mój profil!',
    add_profile:'➕ Dodaj profil', firstname:'👤 Imię',
    native_lang:'🗺️ Język ojczysty', learning_lang:'🌍 Języki do nauki',
    age:'🎂 Twój wiek', avatar:'🎭 Wybierz awatar',
    confirm_pin:'Potwierdź PIN', new_pin:'Nowy PIN',
    export:'💾 Eksportuj', report:'📊 Raport', stop:'⏹ Stop',
    challenge:'Następne wyzwanie →', well_done:'Dobra robota!',
    understood:'Rozumiem ✓', placeholder_name:'Emma, Łukasz, Mama…',
    send_feedback:'Wyślij', feedback_placeholder:'Komentarze, pomysły…',
  },
  RO: {
    start:'▶ Începe!', play:'▶ Joacă!', validate:'✅ Confirmă',
    next:'Următor →', back:'← Înapoi', close:'Închide', cancel:'Anulează',
    correct:'Bravo!', wrong:'Încearcă din nou!', score:'Scor',
    home:'🏠 Acasă', profile:'Profil', settings:'Setări',
    done:'Sesiune terminată!', retry:'Reîncearcă', listen:'🔊 Ascultă',
    hint:'💡 Indiciu', question:'Întrebare', answer:'Răspuns',
    success:'Excelent!', create_profile:'✨ Creează profilul meu!',
    add_profile:'➕ Adaugă profil', firstname:'👤 Prenume',
    native_lang:'🗺️ Limba maternă', learning_lang:'🌍 Limbi de învățat',
    age:'🎂 Vârsta ta', avatar:'🎭 Alege avatarul',
    confirm_pin:'Confirmă PIN', new_pin:'PIN nou',
    export:'💾 Exportă', report:'📊 Raport', stop:'⏹ Stop',
    challenge:'Provocarea următoare →', well_done:'Bine făcut!',
    understood:'Înțeles ✓', placeholder_name:'Emma, Lucas, Mamă…',
    send_feedback:'Trimite', feedback_placeholder:'Comentariile, ideile tale…',
  },
  HU: {
    start:'▶ Kezdés!', play:'▶ Játék!', validate:'✅ Megerősít',
    next:'Tovább →', back:'← Vissza', close:'Bezár', cancel:'Mégsem',
    correct:'Remek!', wrong:'Próbáld újra!', score:'Pontszám',
    home:'🏠 Főoldal', profile:'Profil', settings:'Beállítások',
    done:'Foglalkozás vége!', retry:'Újra', listen:'🔊 Hallgatás',
    hint:'💡 Tipp', question:'Kérdés', answer:'Válasz',
    success:'Kiváló!', create_profile:'✨ Profil létrehozása!',
    add_profile:'➕ Profil hozzáadása', firstname:'👤 Keresztnév',
    native_lang:'🗺️ Anyanyelv', learning_lang:'🌍 Tanulható nyelvek',
    age:'🎂 Korod', avatar:'🎭 Válassz avatárt',
    confirm_pin:'PIN megerősítése', new_pin:'Új PIN',
    export:'💾 Exportálás', report:'📊 Jelentés', stop:'⏹ Stop',
    challenge:'Következő kihívás →', well_done:'Szép munka!',
    understood:'Értettem ✓', placeholder_name:'Emma, Lukács, Anya…',
    send_feedback:'Küldés', feedback_placeholder:'Megjegyzések, ötletek…',
  },
  TR: {
    start:'▶ Başla!', play:'▶ Oyna!', validate:'✅ Onayla',
    next:'İleri →', back:'← Geri', close:'Kapat', cancel:'İptal',
    correct:'Harika!', wrong:'Tekrar dene!', score:'Puan',
    home:'🏠 Ana Sayfa', profile:'Profil', settings:'Ayarlar',
    done:'Oturum tamamlandı!', retry:'Tekrar', listen:'🔊 Dinle',
    hint:'💡 İpucu', question:'Soru', answer:'Cevap',
    success:'Mükemmel!', create_profile:'✨ Profilimi oluştur!',
    add_profile:'➕ Profil ekle', firstname:'👤 Ad',
    native_lang:'🗺️ Ana dil', learning_lang:'🌍 Öğrenilecek diller',
    age:'🎂 Yaşın', avatar:'🎭 Avatarını seç',
    confirm_pin:"PIN'i onayla", new_pin:'Yeni PIN',
    export:'💾 Dışa aktar', report:'📊 Rapor', stop:'⏹ Dur',
    challenge:'Sonraki meydan okuma →', well_done:'Çok iyi!',
    understood:'Anladım ✓', placeholder_name:'Emma, Lucas, Anne…',
    send_feedback:'Gönder', feedback_placeholder:'Yorumlarınız, fikirleriniz…',
  },
};
// Fallback FR pour les langues non encore traduites
['BG','CS','SK','HR','SR','FA'].forEach(function(l){TRANSLATIONS[l]=TRANSLATIONS.FR;});

function T(key) {
  var lang = (typeof P === 'function' && P() && P().native) ? P().native : 'FR';
  var dict = TRANSLATIONS[lang] || TRANSLATIONS.FR;
  return dict[key] || TRANSLATIONS.FR[key] || key;
}

function applyLang() {
  var lang = (typeof P === 'function' && P() && P().native) ? P().native : 'FR';
  document.querySelectorAll('[data-t]').forEach(function(el) {
    var key = el.getAttribute('data-t');
    el.textContent = T(key);
  });
  // Direction RTL pour l'arabe et le persan
  document.documentElement.setAttribute('dir', (lang === 'AR' || lang === 'FA') ? 'rtl' : 'ltr');
}
// ══════════════════════════════════════════════════════════════
"""

marker = 'function loadApp()'
if marker not in content:
    print("❌ marker 'function loadApp()' non trouvé")
    sys.exit(1)

# Insert TRANSLATIONS before loadApp()
content = content.replace(marker, TRANSLATIONS_JS + marker, 1)
print("✅ TRANSLATIONS + T() + applyLang() insérés")

# Add applyLang() call at start of buildHome()
old_bh = 'function buildHome(){'
new_bh = 'function buildHome(){try{applyLang();}catch(e){}'
if old_bh in content:
    content = content.replace(old_bh, new_bh, 1)
    print("✅ applyLang() ajouté dans buildHome()")
else:
    # Try with space
    old_bh2 = 'function buildHome() {'
    if old_bh2 in content:
        content = content.replace(old_bh2, 'function buildHome() {try{applyLang();}catch(e){}', 1)
        print("✅ applyLang() ajouté (variante avec espace)")
    else:
        print("⚠️  buildHome() non trouvé exactement, cherche dans le contenu...")
        idx = content.find('buildHome')
        print(f"   Contexte: {repr(content[idx:idx+50])}")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("✅ index.html sauvegardé")
