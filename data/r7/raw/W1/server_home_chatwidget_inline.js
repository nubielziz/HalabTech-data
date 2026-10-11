/button>
            </div>
            <div class="powered-by">
                Powered by HalabTech AI
            </div>
        </div>
    </div>

    <script>
        // ⚙️ CONFIGURATION
        const WEBHOOK_URL = 'https://chat.halabtech.com';
        
        // 🔐 AUTHENTICATION - Header Auth Key (must match n8n credential)
        const API_KEY = '[REDACTED]'; // ⚠️ Replace with your actual key from n8n
        
        // 🛡️ RATE LIMIT CONFIG
        const RATE_LIMIT = {
            maxMessages: 5,          // Max messages allowed
            windowMs: 30000,         // Time window (30 seconds)
            minDelayMs: 1500,        // Minimum delay between messages (1.5s)
            cooldownMs: 15000        // Cooldown when limit hit (15 seconds)
        };
        
        // 🌍 MULTILINGUAL MESSAGES
        const TRANSLATIONS = {
            en: {
                welcome: `<strong>Hello! 👋</strong><br>I'm the HalabTech AI Assistant.<br><br>How can I help you today?`,
                placeholder: "Type your message...",
                quickActions: [
                    { text: "💰 Services Prices", message: "I want to know about service prices" },
                    { text: "💳 Payment Methods", message: "I want to know about payment methods in my country" },
                    { text: "📦 Order Delay/Issue", message: "I have a delayed order or issue with my order" },
                    { text: "📄 Missing Files/Links", message: "I found missing files or broken links" },
                    { text: "🔧 Technical Issues", message: "I have a technical problem" }
                ]
            },
            ar: {
                welcome: `<strong>مرحباً! 👋</strong><br>أنا مساعد HalabTech الذكي.<br><br>كيف يمكنني مساعدتك اليوم؟`,
                placeholder: "اكتب رسالتك...",
                quickActions: [
                    { text: "💰 أسعار الخدمات", message: "أريد معرفة أسعار الخدمات" },
                    { text: "💳 طرق الدفع", message: "أريد معرفة طرق الدفع في بلدي" },
                    { text: "📦 تأخير/مشكلة طلب", message: "لدي تأخير أو مشكلة في طلبي" },
                    { text: "📄 ملفات/روابط مفقودة", message: "وجدت ملفات مفقودة أو روابط معطلة" },
                    { text: "🔧 مشاكل تقنية", message: "لدي مشكلة تقنية" }
                ]
            },
            tr: {
                welcome: `<strong>Merhaba! 👋</strong><br>Ben HalabTech AI Asistanıyım.<br><br>Size nasıl yardımcı olabilirim?`,
                placeholder: "Mesajınızı yazın...",
                quickActions: [
                    { text: "💰 Hizmet Fiyatları", message: "Hizmet fiyatlarını öğrenmek istiyorum" },
                    { text: "💳 Ödeme Yöntemleri", message: "Ülkemdeki ödeme yöntemlerini öğrenmek istiyorum" },
                    { text: "📦 Sipariş Gecikmesi", message: "Siparişimde gecikme veya sorun var" },
                    { text: "📄 Eksik Dosya/Link", message: "Eksik dosya veya bozuk link buldum" },
                    { text: "🔧 Teknik Sorunlar", message: "Teknik bir sorunum var" }
                ]
            },
            de: {
                welcome: `<strong>Hallo! 👋</strong><br>Ich bin der HalabTech KI-Assistent.<br><br>Wie kann ich Ihnen helfen?`,
                placeholder: "Nachricht eingeben...",
                quickActions: [
                    { text: "💰 Servicepreise", message: "Ich möchte die Servicepreise erfahren" },
                    { text: "💳 Zahlungsmethoden", message: "Ich möchte die Zahlungsmethoden in meinem Land erfahren" },
                    { text: "📦 Bestellverzögerung", message: "Meine Bestellung ist verzögert oder hat ein Problem" },
                    { text: "📄 Fehlende Dateien/Links", message: "Ich habe fehlende Dateien oder defekte Links gefunden" },
                    { text: "🔧 Technische Probleme", message: "Ich habe ein technisches Problem" }
                ]
            },
            fr: {
                welcome: `<strong>Bonjour! 👋</strong><br>Je suis l'assistant IA HalabTech.<br><br>Comment puis-je vous aider?`,
                placeholder: "Tapez votre message...",
                quickActions: [
                    { text: "💰 Prix des services", message: "Je veux connaître les prix des services" },
                    { text: "💳 Méthodes de paiement", message: "Je veux connaître les méthodes de paiement dans mon pays" },
                    { text: "📦 Retard de commande", message: "Ma commande est en retard ou a un problème" },
                    { text: "📄 Fichiers/Liens manquants", message: "J'ai trouvé des fichiers manquants ou des liens cassés" },
                    { text: "🔧 Problèmes techniques", message: "J'ai un problème technique" }
                ]
            },
            es: {
                welcome: `<strong>¡Hola! 👋</strong><br>Soy el asistente de IA de HalabTech.<br><br>¿Cómo puedo ayudarte?`,
                placeholder: "Escribe tu mensaje...",
                quickActions: [
                    { text: "💰 Precios de Servicios", message: "Quiero saber los precios de los servicios" },
                    { text: "💳 Métodos de Pago", message: "Quiero saber los métodos de pago en mi país" },
                    { text: "📦 Retraso de Pedido", message: "Mi pedido está retrasado o tiene un problema" },
                    { text: "📄 Archivos/Enlaces Faltantes", message: "Encontré archivos faltantes o enlaces rotos" },
                    { text: "🔧 Problemas Técnicos", message: "Tengo un problema técnico" }
                ]
            },
            pt: {
                welcome: `<strong>Olá! 👋</strong><br>Sou o assistente de IA da HalabTech.<br><br>Como posso ajudá-lo?`,
                placeholder: "Digite sua mensagem...",
                quickActions: [
                    { text: "💰 Preços dos Serviços", message: "Quero saber os preços dos serviços" },
                    { text: "💳 Métodos de Pagamento", message: "Quero saber os métodos de pagamento no meu país" },
                    { text: "📦 Atraso no Pedido", message: "Meu pedido está atrasado ou tem um problema" },
                    { text: "📄 Arquivos/Links Faltando", message: "Encontrei arquivos faltando ou links quebrados" },
                    { text: "🔧 Problemas Técnicos", message: "Tenho um problema técnico" }
                ]
            },
            it: {
                welcome: `<strong>Ciao! 👋</strong><br>Sono l'assistente AI di HalabTech.<br><br>Come posso aiutarti?`,
                placeholder: "Scrivi il tuo messaggio...",
                quickActions: [
                    { text: "💰 Prezzi Servizi", message: "Voglio sapere i prezzi dei servizi" },
                    { text: "💳 Metodi di Pagamento", message: "Voglio sapere i metodi di pagamento nel mio paese" },
                    { text: "📦 Ritardo Ordine", message: "Il mio ordine è in ritardo o ha un problema" },
                    { text: "📄 File/Link Mancanti", message: "Ho trovato file mancanti o link rotti" },
                    { text: "🔧 Problemi Tecnici", message: "Ho un problema tecnico" }
                ]
            },
            nl: {
                welcome: `<strong>Hallo! 👋</strong><br>Ik ben de HalabTech AI-assistent.<br><br>Hoe kan ik u helpen?`,
                placeholder: "Typ uw bericht...",
                quickActions: [
                    { text: "💰 Serviceprijzen", message: "Ik wil de serviceprijzen weten" },
                    { text: "💳 Betaalmethoden", message: "Ik wil de betaalmethoden in mijn land weten" },
                    { text: "📦 Bestelvertraging", message: "Mijn bestelling is vertraagd of heeft een probleem" },
                    { text: "📄 Ontbrekende Bestanden", message: "Ik vond ontbrekende bestanden of kapotte links" },
                    { text: "🔧 Technische Problemen", message: "Ik heb een technisch probleem" }
                ]
            },
            ru: {
                welcome: `<strong>Привет! 👋</strong><br>Я AI-ассистент HalabTech.<br><br>Чем могу помочь?`,
                placeholder: "Введите сообщение...",
                quickActions: [
                    { text: "💰 Цены на услуги", message: "Хочу узнать цены на услуги" },
                    { text: "💳 Способы оплаты", message: "Хочу узнать способы оплаты в моей стране" },
                    { text: "📦 Задержка заказа", message: "Мой заказ задерживается или есть проблема" },
                    { text: "📄 Отсутствующие файлы", message: "Нашел отсутствующие файлы или битые ссылки" },
                    { text: "🔧 Технические проблемы", message: "У меня техническая проблема" }
                ]
            },
            uk: {
                welcome: `<strong>Привіт! 👋</strong><br>Я AI-асистент HalabTech.<br><br>Чим можу допомогти?`,
                placeholder: "Введіть повідомлення...",
                quickActions: [
                    { text: "💰 Ціни на послуги", message: "Хочу дізнатися ціни на послуги" },
                    { text: "💳 Способи оплати", message: "Хочу дізнатися способи оплати в моїй країні" },
                    { text: "📦 Затримка замовлення", message: "Моє замовлення затримується або є проблема" },
                    { text: "📄 Відсутні файли", message: "Знайшов відсутні файли або биті посилання" },
                    { text: "🔧 Технічні проблеми", message: "У мене технічна проблема" }
                ]
            },
            pl: {
                welcome: `<strong>Cześć! 👋</strong><br>Jestem asystentem AI HalabTech.<br><br>Jak mogę pomóc?`,
                placeholder: "Wpisz wiadomość...",
                quickActions: [
                    { text: "💰 Ceny usług", message: "Chcę poznać ceny usług" },
                    { text: "💳 Metody płatności", message: "Chcę poznać metody płatności w moim kraju" },
                    { text: "📦 Opóźnienie zamówienia", message: "Moje zamówienie jest opóźnione lub ma problem" },
                    { text: "📄 Brakujące pliki", message: "Znalazłem brakujące pliki lub zepsute linki" },
                    { text: "🔧 Problemy techniczne", message: "Mam problem techniczny" }
                ]
            },
            cs: {
                welcome: `<strong>Ahoj! 👋</strong><br>Jsem AI asistent HalabTech.<br><br>Jak vám mohu pomoci?`,
                placeholder: "Napište zprávu...",
                quickActions: [
                    { text: "💰 Ceny služeb", message: "Chci znát ceny služeb" },
                    { text: "💳 Platební metody", message: "Chci znát platební metody v mé zemi" },
                    { text: "📦 Zpoždění objednávky", message: "Moje objednávka je zpožděná nebo má problém" },
                    { text: "📄 Chybějící soubory", message: "Našel jsem chybějící soubory nebo nefunkční odkazy" },
                    { text: "🔧 Technické problémy", message: "Mám technický problém" }
                ]
            },
            he: {
                welcome: `<strong>שלום! 👋</strong><br>אני העוזר החכם של HalabTech.<br><br>איך אוכל לעזור?`,
                placeholder: "הקלד הודעה...",
                quickActions: [
                    { text: "💰 מחירי שירותים", message: "אני רוצה לדעת את מחירי השירותים" },
                    { text: "💳 אמצעי תשלום", message: "אני רוצה לדעת את אמצעי התשלום בארץ שלי" },
                    { text: "📦 עיכוב הזמנה", message: "ההזמנה שלי מתעכבת או יש בעיה" },
                    { text: "📄 קבצים חסרים", message: "מצאתי קבצים חסרים או קישורים שבורים" },
                    { text: "🔧 בעיות טכניות", message: "יש לי בעיה טכנית" }
                ]
            },
            zh: {
                welcome: `<strong>你好！👋</strong><br>我是 HalabTech AI 助手。<br><br>我能为您提供什么帮助？`,
                placeholder: "输入您的消息...",
                quickActions: [
                    { text: "💰 服务价格", message: "我想了解服务价格" },
                    { text: "💳 付款方式", message: "我想了解我所在国家的付款方式" },
                    { text: "📦 订单延迟/问题", message: "我的订单延迟或有问题" },
                    { text: "📄 缺失文件/链接", message: "我发现缺失文件或损坏的链接" },
                    { text: "🔧 技术问题", message: "我有技术问题" }
                ]
            },
            ja: {
                welcome: `<strong>こんにちは！👋</strong><br>HalabTech AIアシスタントです。<br><br>何をお手伝いできますか？`,
                placeholder: "メッセージを入力...",
                quickActions: [
                    { text: "💰 サービス価格", message: "サービス価格について知りたいです" },
                    { text: "💳 支払い方法", message: "私の国での支払い方法について知りたいです" },
                    { text: "📦 注文遅延/問題", message: "注文が遅れているか問題があります" },
                    { text: "📄 ファイル/リンク不足", message: "ファイルの欠落やリンク切れを見つけました" },
                    { text: "🔧 技術的問題", message: "技術的な問題があります" }
                ]
            },
            ko: {
                welcome: `<strong>안녕하세요! 👋</strong><br>HalabTech AI 어시스턴트입니다.<br><br>무엇을 도와드릴까요?`,
                placeholder: "메시지를 입력하세요...",
                quickActions: [
                    { text: "💰 서비스 가격", message: "서비스 가격을 알고 싶습니다" },
                    { text: "💳 결제 방법", message: "제 나라의 결제 방법을 알고 싶습니다" },
                    { text: "📦 주문 지연/문제", message: "주문이 지연되거나 문제가 있습니다" },
                    { text: "📄 누락된 파일/링크", message: "누락된 파일이나 깨진 링크를 발견했습니다" },
                    { text: "🔧 기술적 문제", message: "기술적인 문제가 있습니다" }
                ]
            },
            th: {
                welcome: `<strong>สวัสดี! 👋</strong><br>ฉันคือผู้ช่วย AI ของ HalabTech<br><br>ฉันช่วยอะไรคุณได้บ้าง?`,
                placeholder: "พิมพ์ข้อความของคุณ...",
                quickActions: [
                    { text: "💰 ราคาบริการ", message: "ฉันต้องการทราบราคาบริการ" },
                    { text: "💳 วิธีการชำระเงิน", message: "ฉันต้องการทราบวิธีการชำระเงินในประเทศของฉัน" },
                    { text: "📦 คำสั่งซื้อล่าช้า", message: "คำสั่งซื้อของฉันล่าช้าหรือมีปัญหา" },
                    { text: "📄 ไฟล์/ลิงก์หายไป", message: "ฉันพบไฟล์หายไปหรือลิงก์เสีย" },
                    { text: "🔧 ปัญหาทางเทคนิค", message: "ฉันมีปัญหาทางเทคนิค" }
                ]
            },
            vi: {
                welcome: `<strong>Xin chào! 👋</strong><br>Tôi là trợ lý AI của HalabTech.<br><br>Tôi có thể giúp gì cho bạn?`,
                placeholder: "Nhập tin nhắn...",
                quickActions: [
                    { text: "💰 Giá dịch vụ", message: "Tôi muốn biết giá dịch vụ" },
                    { text: "💳 Phương thức thanh toán", message: "Tôi muốn biết phương thức thanh toán ở nước tôi" },
                    { text: "📦 Đơn hàng chậm trễ", message: "Đơn hàng của tôi bị chậm trễ hoặc có vấn đề" },
                    { text: "📄 File/Link bị thiếu", message: "Tôi tìm thấy file bị thiếu hoặc link hỏng" },
                    { text: "🔧 Vấn đề kỹ thuật", message: "Tôi có vấn đề kỹ thuật" }
                ]
            },
            sv: {
                welcome: `<strong>Hej! 👋</strong><br>Jag är HalabTech AI-assistenten.<br><br>Hur kan jag hjälpa dig?`,
                placeholder: "Skriv ditt meddelande...",
                quickActions: [
                    { text: "💰 Tjänstepriser", message: "Jag vill veta tjänstepriserna" },
                    { text: "💳 Betalningsmetoder", message: "Jag vill veta betalningsmetoderna i mitt land" },
                    { text: "📦 Orderfördröjning", message: "Min order är försenad eller har ett problem" },
                    { text: "📄 Saknade filer/länkar", message: "Jag hittade saknade filer eller trasiga länkar" },
                    { text: "🔧 Tekniska problem", message: "Jag har ett tekniskt problem" }
                ]
            },
            da: {
                welcome: `<strong>Hej! 👋</strong><br>Jeg er HalabTech AI-assistenten.<br><br>Hvordan kan jeg hjælpe?`,
                placeholder: "Skriv din besked...",
                quickActions: [
                    { text: "💰 Servicepriser", message: "Jeg vil gerne vide servicepriserne" },
                    { text: "💳 Betalingsmetoder", message: "Jeg vil gerne vide betalingsmetoderne i mit land" },
                    { text: "📦 Ordreforsinkelse", message: "Min ordre er forsinket eller har et problem" },
                    { text: "📄 Manglende filer/links", message: "Jeg fandt manglende filer eller ødelagte links" },
                    { text: "🔧 Tekniske problemer", message: "Jeg har et teknisk problem" }
                ]
            }
        };
        
        // Detect browser language
        function getBrowserLanguage() {
            const lang = navigator.language || navigator.userLanguage || 'en';
            const shortLang = lang.split('-')[0].toLowerCase();
            return TRANSLATIONS[shortLang] ? shortLang : 'en';
        }
        
        const userLang = getBrowserLanguage();
        const t = TRANSLATIONS[userLang];
        
        // Set HTML language attribute (but keep direction dynamic per message)
        document.documentElement.setAttribute('lang', userLang);
        document.documentElement.setAttribute('dir', 'ltr'); // Default to LTR for UI elements
        
        // Session management
        let sessionId = localStorage.getItem('halabtech_chat_session');
        if (!sessionId) {
            sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
            localStorage.setItem('halabtech_chat_session', sessionId);
        }
        
        // 🛡️ Rate Limit State (persisted in sessionStorage)
        let messageTimestamps = JSON.parse(sessionStorage.getItem('chat_rate_limit') || '[]');
        let lastMessageTime = parseInt(sessionStorage.getItem('chat_last_msg') || '0');
        let cooldownUntil = parseInt(sessionStorage.getItem('chat_cooldown') || '0');
        let cooldownInterval = null;
        
        // DOM Elements
        const chatWidget = document.getElementById('chatWidget');
        const chatFloatButton = document.getElementById('chatFloatButton');
        const closeBtn = document.getElementById('closeBtn');
        const refreshBtn = document.getElementById('refreshBtn');
        const themeBtn = document.getElementById('themeBtn');
        const chatMessages = document.getElementById('chatMessages');
        const chatInput = document.getElementById('chatInput');
        const sendButton = document.getElementById('sendButton');
        const typingIndicator = document.getElementById('typingIndicator');
        const errorToast = document.getElementById('errorToast');
        const formIndicator = document.getElementById('formIndicator');
        const formTitle = document.getElementById('formTitle');
        const formStatus = document.getElementById('formStatus');
        const formExitBtn = document.getElementById('formExitBtn');
        
        // 🌙 THEME MANAGEMENT
        let isDarkMode = localStorage.getItem('halabtech_dark_mode') === 'true';
        
        function applyTheme() {
            if (isDarkMode) {
                chatWidget.classList.add('dark-mode');
                themeBtn.querySelector('.sun-icon').style.display = 'none';
                themeBtn.querySelector('.moon-icon').style.display = 'block';
            } else {
                chatWidget.classList.remove('dark-mode');
                themeBtn.querySelector('.sun-icon').style.display = 'block';
                themeBtn.querySelector('.moon-icon').style.display = 'none';
            }
        }
        
        function toggleTheme() {
            isDarkMode = !isDarkMode;
            localStorage.setItem('halabtech_dark_mode', isDarkMode.toString());
            applyTheme();
        }
        
        // Apply theme on load
        applyTheme();
        themeBtn.addEventListener('click', toggleTheme);
        
        // State
        let isOpen = false;
        
        // 📋 FORM FLOW STATE
        let isInFormFlow = false;
        let currentFormName = '';
        let currentFormStep = '';
        
        // Form flow translations
        const FORM_TRANSLATIONS = {
            en: {
                inProgress: 'Form in Progress',
                waitingResponse: 'Waiting for your response...',
                exitForm: 'Exit Form',
                exitConfirm: 'Are you sure you want to exit the form?',
                formExited: '✅ Form cancelled. You can start a new conversation.',
                processingStep: 'Processing step...'
            },
            ar: {
                inProgress: 'نموذج قيد التقدم',
                waitingResponse: 'في انتظار ردك...',
                exitForm: 'إلغاء النموذج',
                exitConfirm: 'هل أنت متأكد أنك تريد إلغاء النموذج؟',
                formExited: '✅ تم إلغاء النموذج. يمكنك بدء محادثة جديدة.',
                processingStep: 'جاري معالجة الخطوة...'
            },
            tr: {
                inProgress: 'Form Devam Ediyor',
                waitingResponse: 'Yanıtınız bekleniyor...',
                exitForm: 'Formu İptal Et',
                exitConfirm: 'Formu iptal etmek istediğinizden emin misiniz?',
                formExited: '✅ Form iptal edildi. Yeni bir konuşma başlatabilirsiniz.',
                processingStep: 'Adım işleniyor...'
            },
            de: {
                inProgress: 'Formular läuft',
                waitingResponse: 'Warten auf Ihre Antwort...',
                exitForm: 'Formular beenden',
                exitConfirm: 'Möchten Sie das Formular wirklich beenden?',
                formExited: '✅ Formular abgebrochen. Sie können ein neues Gespräch beginnen.',
                processingStep: 'Schritt wird verarbeitet...'
            },
            fr: {
                inProgress: 'Formulaire en cours',
                waitingResponse: 'En attente de votre réponse...',
                exitForm: 'Quitter le formulaire',
                exitConfirm: 'Êtes-vous sûr de vouloir quitter le formulaire?',
                formExited: '✅ Formulaire annulé. Vous pouvez commencer une nouvelle conversation.',
                processingStep: 'Traitement de l\'étape...'
            },
            es: {
                inProgress: 'Formulario en progreso',
                waitingResponse: 'Esperando tu respuesta...',
                exitForm: 'Salir del formulario',
                exitConfirm: '¿Estás seguro de que quieres salir del formulario?',
                formExited: '✅ Formulario cancelado. Puedes iniciar una nueva conversación.',
                processingStep: 'Procesando paso...'
            }
        };
        
        // Get form translations (fallback to English)
        const ft = FORM_TRANSLATIONS[userLang] || FORM_TRANSLATIONS.en;
        
        // 📋 FORM FLOW FUNCTIONS
        function showFormIndicator(formName = null, stepInfo = null) {
            isInFormFlow = true;
            currentFormName = formName || ft.inProgress;
            currentFormStep = stepInfo || ft.waitingResponse;
            
            formTitle.textContent = currentFormName;
            formStatus.textContent = currentFormStep;
            formIndicator.classList.add('active');
            
            // Save form state to session
            sessionStorage.setItem('chat_form_active', 'true');
            sessionStorage.setItem('chat_form_name', currentFormName);
            sessionStorage.setItem('chat_form_step', currentFormStep);
        }
        
        function hideFormIndicator() {
            isInFormFlow = false;
            currentFormName = '';
            currentFormStep = '';
            
            formIndicator.classList.remove('active');
            
            // Clear form state from session
            sessionStorage.removeItem('chat_form_active');
            sessionStorage.removeItem('chat_form_name');
            sessionStorage.removeItem('chat_form_step');
        }
        
        function updateFormStatus(stepInfo) {
            if (isInFormFlow) {
                currentFormStep = stepInfo;
                formStatus.textContent = stepInfo;
                sessionStorage.setItem('chat_form_step', stepInfo);
            }
        }
        
        async function exitFormFlow() {
            // Show confirmation (optional - can be removed for instant exit)
            // if (!confirm(ft.exitConfirm)) return;
            
            // Disable exit button while processing
            formExitBtn.disabled = true;
            formExitBtn.textContent = '...';
            
            try {
                // Send exit signal to backend to clear form state
                await fetch(WEBHOOK_URL, {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'X-Api-Key': API_KEY  // 🔐 Authentication header
                    },
                    body: JSON.stringify({
                        message: '__EXIT_FORM__',
                        session_id: sessionId,
                        action: 'exit_form',
                        timestamp: new Date().toISOString()
                    })
                });
            } catch (error) {
                console.log('Form exit signal sent (server may not support it)');
            }
            
            // Hide the form indicator
            hideFormIndicator();
            
            // Show exit confirmation message
            addMessage(ft.formExited, 'bot');
            
            // Re-enable input
            chatInput.disabled = false;
            sendButton.disabled = false;
            chatInput.focus();
            
            // Reset exit button
            formExitBtn.disabled = false;
            formExitBtn.innerHTML = `
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
                ${ft.exitForm}
            `;
        }
        
        // Detect form flow from bot response
        function detectFormFlow(response) {
            // Check for form indicators in the response
            // These can be customized based on your backend's response format
            
            // Method 1: Check for explicit form_active flag in response
            if (response.form_active === true || response.in_form === true) {
                showFormIndicator(response.form_name, response.form_step || response.current_step);
                return;
            }
            
            // Method 2: Check for form_active === false to hide indicator
            if (response.form_active === false || response.in_form === false || response.form_completed === true) {
                hideFormIndicator();
                return;
            }
            
            // Method 3: Detect common form patterns in message text
            const message = (response.message || '').toLowerCase();
            const formPatterns = [
                /please (provide|enter|type|share|give)/i,
                /what is your/i,
                /enter your/i,
                /please confirm/i,
                /step \d+ of \d+/i,
                /next,? (please )?(provide|enter|tell)/i,
                /(email|phone|name|address|number).*:/i,
                /waiting for/i,
                /please respond with/i
            ];
            
            const formEndPatterns = [
                /thank you for (providing|submitting|completing)/i,
                /your (request|form|submission) has been/i,
                /successfully (submitted|completed|received)/i,
                /we('ve| have) received your/i,
                /form completed/i,
                /all done/i
            ];
            
            // Check if this looks like form completion
            for (const pattern of formEndPatterns) {
                if (pattern.test(message)) {
                    hideFormIndicator();
                    return;
                }
            }
            
            // Check if this looks like a form prompt
            for (const pattern of formPatterns) {
                if (pattern.test(message)) {
                    if (!isInFormFlow) {
                        showFormIndicator();
                    } else {
                        updateFormStatus(ft.waitingResponse);
                    }
                    return;
                }
            }
        }
        
        // Restore form state on page load
        function restoreFormState() {
            const formActive = sessionStorage.getItem('chat_form_active');
            if (formActive === 'true') {
                const formName = sessionStorage.getItem('chat_form_name');
                const formStep = sessionStorage.getItem('chat_form_step');
                showFormIndicator(formName, formStep);
            }
        }
        
        // Initialize form exit button listener
        formExitBtn.addEventListener('click', exitFormFlow);
        
        // Set localized exit button text
        formExitBtn.innerHTML = `
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
            ${ft.exitForm}
        `;
        
        // Restore form state on load
        restoreFormState();
        
        // 🛡️ RATE LIMITING FUNCTIONS
        function cleanOldTimestamps() {
            const now = Date.now();
            messageTimestamps = messageTimestamps.filter(ts => now - ts < RATE_LIMIT.windowMs);
            sessionStorage.setItem('chat_rate_limit', JSON.stringify(messageTimestamps));
        }
        
        function isRateLimited() {
            const now = Date.now();
            
            // Check cooldown first
            if (now < cooldownUntil) {
                return { limited: true, reason: 'cooldown', remaining: Math.ceil((cooldownUntil - now) / 1000) };
            }
            
            // Check minimum delay between messages
            if (lastMessageTime && (now - lastMessageTime) < RATE_LIMIT.minDelayMs) {
                return { limited: true, reason: 'too_fast', remaining: 1 };
            }
            
            // Clean old timestamps and check message count
            cleanOldTimestamps();
            
            if (messageTimestamps.length >= RATE_LIMIT.maxMessages) {
                // Set cooldown
                cooldownUntil = now + RATE_LIMIT.cooldownMs;
                sessionStorage.setItem('chat_cooldown', cooldownUntil.toString());
                startCooldownTimer();
                return { limited: true, reason: 'limit_reached', remaining: Math.ceil(RATE_LIMIT.cooldownMs / 1000) };
            }
            
            return { limited: false };
        }
        
        function recordMessage() {
            const now = Date.now();
            messageTimestamps.push(now);
            lastMessageTime = now;
            sessionStorage.setItem('chat_rate_limit', JSON.stringify(messageTimestamps));
            sessionStorage.setItem('chat_last_msg', now.toString());
        }
        
        function showRateLimitWarning(seconds, reason) {
            let message = '';
            switch(reason) {
                case 'cooldown':
                case 'limit_reached':
                    message = `⏳ Slow down! Wait ${seconds}s`;
                    break;
                case 'too_fast':
                    message = '⚡ Too fast! Wait a moment';
                    break;
            }
            errorToast.innerHTML = `<span>🛡️</span> ${message}`;
            errorToast.style.background = '#fef3c7';
            errorToast.style.color = '#92400e';
            errorToast.classList.add('active');
        }
        
        function hideRateLimitWarning() {
            errorToast.classList.remove('active');
            // Reset to default error style
            setTimeout(() => {
                errorToast.innerHTML = '<span>⚠️</span> Failed to send message';
                errorToast.style.background = '#fee2e2';
                errorToast.style.color = '#991b1b';
            }, 300);
        }
        
        function startCooldownTimer() {
            if (cooldownInterval) clearInterval(cooldownInterval);
            
            updateCooldownDisplay();
            
            cooldownInterval = setInterval(() => {
                const now = Date.now();
                if (now >= cooldownUntil) {
                    clearInterval(cooldownInterval);
                    cooldownInterval = null;
                    hideRateLimitWarning();
                    sendButton.disabled = false;
                    chatInput.disabled = false;
                } else {
                    updateCooldownDisplay();
                }
            }, 1000);
        }
        
        function updateCooldownDisplay() {
            const remaining = Math.ceil((cooldownUntil - Date.now()) / 1000);
            if (remaining > 0) {
                showRateLimitWarning(remaining, 'cooldown');
                sendButton.disabled = true;
                chatInput.disabled = true;
            }
        }
        
        // Check for existing cooldown on page load
        if (Date.now() < cooldownUntil) {
            startCooldownTimer();
        }
        
        // 🎯 QUICK ACTIONS
        const quickActionsContainer = document.getElementById('quickActions');
        
        function renderQuickActions() {
            if (!quickActionsContainer || !t.quickActions) return;
            
            quickActionsContainer.innerHTML = '';
            t.quickActions.forEach((action) => {
                const btn = document.createElement('button');
                btn.className = 'quick-action-btn';
                btn.textContent = action.text;
                btn.addEventListener('click', () => handleQuickAction(action.message));
                quickActionsContainer.appendChild(btn);
            });
        }
        
        function handleQuickAction(message) {
            // Hide quick actions after clicking
            if (quickActionsContainer) {
                quickActionsContainer.style.display = 'none';
            }
            
            // Set the message in input and send
            chatInput.value = message;
            sendMessage();
        }
        
        function showQuickActions() {
            if (quickActionsContainer) {
                quickActionsContainer.style.display = 'flex';
                renderQuickActions();
            }
        }
        
        // 🌍 Set welcome message and placeholder based on browser language
        document.addEventListener('DOMContentLoaded', function() {
            const welcomeMsg = document.querySelector('#welcomeMessage .message-bubble');
            if (welcomeMsg) {
                welcomeMsg.innerHTML = t.welcome;
                // Apply text direction to welcome message
                const direction = detectTextDirection(t.welcome);
                welcomeMsg.classList.add(direction);
            }
            chatInput.placeholder = t.placeholder;
            renderQuickActions();
        });
        
        // Also set immediately in case DOM is already loaded
        const welcomeMsg = document.querySelector('#welcomeMessage .message-bubble');
        if (welcomeMsg) {
            welcomeMsg.innerHTML = t.welcome;
            // Apply text direction to welcome message
            const direction = detectTextDirection(t.welcome);
            welcomeMsg.classList.add(direction);
        }
        if (chatInput) {
            chatInput.placeholder = t.placeholder;
        }
        renderQuickActions();
        
        // Toggle Chat
        function toggleChat() {
            isOpen = !isOpen;
            if (isOpen) {
                chatWidget.classList.remove('minimized');
                chatFloatButton.classList.add('hidden');
                setTimeout(() => chatInput.focus(), 300);
                // Notify parent page (iframe support)
                if (window.parent !== window) {
                    window.parent.postMessage('chatOpened', '*');
                }
            } else {
                chatWidget.classList.add('minimized');
                chatFloatButton.classList.remove('hidden');
                // Notify parent page (iframe support)
                if (window.parent !== window) {
                    window.parent.postMessage('chatClosed', '*');
                }
            }
        }
        
        // Listen for close message from parent page (iframe support)
        window.addEventListener('message', function(e) {
            if (e.data === 'closeChat' && isOpen) {
                toggleChat();
            }
        });
        
        chatFloatButton.addEventListener('click', toggleChat);
        closeBtn.addEventListener('click', toggleChat);
        
        // 🔄 Restart Conversation
        function restartConversation() {
            // Generate new session ID
            sessionId = `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
            localStorage.setItem('halabtech_chat_session', sessionId);
            
            // Clear all messages except welcome message
            const messages = chatMessages.querySelectorAll('.message:not(#welcomeMessage)');
            messages.forEach(msg => msg.remove());
            
            // Reset welcome message
            const welcomeMsg = document.querySelector('#welcomeMessage .message-bubble');
            if (welcomeMsg) {
                welcomeMsg.innerHTML = t.welcome;
                // Reapply text direction
                welcomeMsg.className = 'message-bubble';
                const direction = detectTextDirection(t.welcome);
                welcomeMsg.classList.add(direction);
            }
            const welcomeTime = document.querySelector('#welcomeMessage .message-time');
            if (welcomeTime) {
                welcomeTime.textContent = 'Just now';
            }
            
            // Show quick actions again
            showQuickActions();
            
            // Hide form indicator if active
            hideFormIndicator();
            
            // Clear rate limit state for new session
            messageTimestamps = [];
            lastMessageTime = 0;
            cooldownUntil = 0;
            sessionStorage.removeItem('chat_rate_limit');
            sessionStorage.removeItem('chat_last_msg');
            sessionStorage.removeItem('chat_cooldown');
            
            // Re-enable input
            chatInput.disabled = false;
            sendButton.disabled = false;
            chatInput.value = '';
            chatInput.focus();
            
            // Visual feedback - spin the refresh button
            refreshBtn.style.transform = 'rotate(360deg)';
            setTimeout(() => {
                refreshBtn.style.transform = '';
            }, 300);
        }
        
        refreshBtn.addEventListener('click', restartConversation);

        // Close on click outside (works both standalone and in iframe)
        document.addEventListener('click', (e) => {
            if (isOpen && 
                !chatWidget.contains(e.target) && 
                !chatFloatButton.contains(e.target)) {
                toggleChat();
            }
        });
        
        // For iframe: close when clicking the transparent area around the widget
        document.body.addEventListener('click', (e) => {
            if (isOpen && e.target === document.body) {
                toggleChat();
            }
        });
        
        // Detect if text is RTL (Arabic, Hebrew, Persian, Urdu, etc.)
        function detectTextDirection(text) {
            // Remove HTML tags and special characters for better detection
            const cleanText = text.replace(/<[^>]*>/g, '').replace(/[^\w\s]/g, '');
            
            // RTL Unicode ranges:
            // Arabic: \u0600-\u06FF
            // Hebrew: \u0590-\u05FF
            // Arabic Supplement: \u0750-\u077F
            // Arabic Extended: \u08A0-\u08FF
            const rtlRegex = /[\u0590-\u05FF\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]/;
            
            // Check if text contains RTL characters
            return rtlRegex.test(cleanText) ? 'rtl' : 'ltr';
        }
        
        // Format Message
        function formatMessage(text) {
            let formatted = text
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank">$1</a>')
                .replace(/\n/g, '<br>');
            return formatted;
        }
        
        // Add Message
        function addMessage(text, sender = 'bot') {
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}`;
            
            const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            
            const bubbleContent = sender === 'bot' ? formatMessage(text) : text;
            
            // Detect text direction for this specific message
            const textDirection = detectTextDirection(text);
            
            messageDiv.innerHTML = `
                <div class="message-bubble ${textDirection}">${bubbleContent}</div>
                <div class="message-time">${time}</div>
            `;
            
            // Insert before typing indicator
            chatMessages.insertBefore(messageDiv, typingIndicator);
            
            if (sender === 'user') {
                scrollToBottom();
            } else {
                // For bot messages, especially long ones, scroll to the start of the message
                // Use a small timeout to ensure rendering is complete
                setTimeout(() => {
                    messageDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }, 10);
            }
        }
        
        function scrollToBottom() {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }
        
        function showTyping() {
            typingIndicator.classList.add('active');
            scrollToBottom();
        }
        
        function hideTyping() {
            typingIndicator.classList.remove('active');
        }
        
        // Send Message
        async function sendMessage() {
            const text = chatInput.value.trim();
            if (!text) return;
            
            // 🛡️ CHECK RATE LIMIT
            const rateLimitCheck = isRateLimited();
            if (rateLimitCheck.limited) {
                showRateLimitWarning(rateLimitCheck.remaining, rateLimitCheck.reason);
                
                // Auto-hide after showing (unless it's a cooldown)
                if (rateLimitCheck.reason === 'too_fast') {
                    setTimeout(hideRateLimitWarning, 2000);
                }
                return;
            }
            
            // 🛡️ Record this message for rate limiting
            recordMessage();
            
            addMessage(text, 'user');
            chatInput.value = '';
            showTyping();
            
            sendButton.disabled = true;
            chatInput.disabled = true;
            hideRateLimitWarning();
            
            try {
                const response = await fetch(WEBHOOK_URL, {
                    method: 'POST',
                    headers: { 
                        'Content-Type': 'application/json',
                        'X-Api-Key': API_KEY  // 🔐 Authentication header
                    },
                    body: JSON.stringify({
                        message: text,
                        session_id: sessionId,
                        timestamp: new Date().toISOString()
                    })
                });
                
                // 🛡️ Handle server-side rate limiting (429)
                if (response.status === 429) {
                    hideTyping();
                    const data = await response.json();
                    const retryAfter = data.retryAfter || 60;
                    
                    // Set server-side cooldown
                    cooldownUntil = Date.now() + (retryAfter * 1000);
                    sessionStorage.setItem('chat_cooldown', cooldownUntil.toString());
                    startCooldownTimer();
                    
                    // Show server rate limit message
                    addMessage('⏳ ' + (data.message || `Too many messages. Please wait ${retryAfter} seconds.`), 'bot');
                    return;
                }
                
                if (!response.ok) throw new Error('Network response was not ok');
                
                const data = await response.json();
                hideTyping();
                
                // Check if response indicates rate limit (for non-429 rate limit responses)
                if (data.error === 'rate_limit' || data.error === 'rate_limit_exceeded') {
                    const retryAfter = data.retryAfter || 60;
                    cooldownUntil = Date.now() + (retryAfter * 1000);
                    sessionStorage.setItem('chat_cooldown', cooldownUntil.toString());
                    startCooldownTimer();
                    addMessage('⏳ ' + (data.message || `Please slow down. Wait ${retryAfter} seconds.`), 'bot');
                    return;
                }
                
                // 📋 Detect form flow from response
                detectFormFlow(data);
                
                addMessage(data.message || 'I received your message!', 'bot');
                
                if (data.session_id) {
                    sessionId = data.session_id;
                    localStorage.setItem('halabtech_chat_session', sessionId);
                }
                
            } catch (error) {
                console.error('Error:', error);
                hideTyping();
                // Show network error (not rate limit)
                errorToast.innerHTML = '<span>⚠️</span> Failed to send message';
                errorToast.style.background = '#fee2e2';
                errorToast.style.color = '#991b1b';
                errorToast.classList.add('active');
                setTimeout(() => errorToast.classList.remove('active'), 3000);
            } finally {
                sendButton.disabled = false;
                chatInput.disabled = false;
                chatInput.focus();
                scrollToBottom();
            }
        }
        
        // Listeners
        sendButton.addEventListener('click', sendMessage);
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
        
        // Auto-open on first visit
        if (!localStorage.getItem('halabtech_chat_visited')) {
            setTimeout(() => {
                // toggleChat(); // Optional: Uncomment to auto-open
                localStorage.setItem('halabtech_chat_visited', 'true');
            }, 2000);
        }
    