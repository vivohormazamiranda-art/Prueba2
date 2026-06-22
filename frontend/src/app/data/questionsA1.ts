export interface Question {
  id: number;

  // Nivel MCER
  level: 'A1' | 'A2' | 'B1' | 'B2' | 'C1' | 'C2';

  // Habilidad evaluada
  skill:
    | 'grammar'
    | 'vocabulary'
    | 'reading'
    | 'writing'
    | 'speaking'
    | 'listening';

  // Tipo de pregunta
  type:
    | 'multiple'
    | 'writing'
    | 'speaking'
    | 'listening'
    | 'reading'
    | 'image';

  category: string;

  question: string;

  // Texto de apoyo (para Reading)
  text?: string;

  // Instrucciones adicionales
  prompt?: string;

  // Opciones
  options?: string[];

  correctAnswer?: number | string;

  // ---------- Recursos multimedia ----------

  // Imagen opcional
  image?: {
    url: string;
    alt?: string;
  };

  // Audio opcional
  audio?: {
    url: string;
    duration?: number;
    transcript?: string;
  };

  // Video opcional
  video?: {
    url: string;
  };

  // ---------- Configuración ----------

  points: number;

  timeLimit?: number;

  explanation?: string;
}

export const questions: Question[] = [
  // Easy - Vocabulario
  {
    type: 'multiple',
    id: 1,
    level: 'A2',
    skill: 'vocabulary',
    question: "What is the opposite of 'hot'?",
    options: ['Warm', 'Cold', 'Sunny', 'Dry'],
    correctAnswer: 1,
    points: 5,
    category: 'Vocabulary',
  },
  {
    type: 'multiple',
    id: 2,
    level: 'A2',
    skill: 'vocabulary',
    question: "What is the synonym of 'happy'?",
    options: ['Sad', 'Angry', 'Joyful', 'Tired'],
    correctAnswer: 2,
    points: 5,
    category: 'Vocabulary',
  },
  {
    type: 'multiple',
    id: 3,
    level: 'A2',
    skill: 'grammar',
    question: "Choose the correct article: '__ apple a day keeps the doctor away'",
    options: ['A', 'An', 'The', 'No article'],
    correctAnswer: 1,
    points: 5,
    category: 'Grammar',
  },
  {
    type: 'multiple',
    id: 4,
    level: 'A2',
    skill: 'vocabulary',
    question: "What does 'big' mean?",
    options: ['Small', 'Large', 'Fast', 'Slow'],
    correctAnswer: 1,
    points: 5,
    category: 'Vocabulary',
  },
  {
    type: 'multiple',
    id: 5,
    level: 'A2',
    skill: 'grammar',
    question: "Complete: 'She ___ to school every day'",
    options: ['go', 'goes', 'going', 'gone'],
    correctAnswer: 1,
    points: 5,
    category: 'Grammar',
  },
  
  // Medium - Gramática
  {
    type: 'multiple',
    id: 6,
    level: 'B1',
    skill: 'grammar',
    question: "If I _____ known about the party, I would have gone.",
    options: ['knew', 'had known', 'have known', 'would know'],
    correctAnswer: 1,
    points: 10,
    category: 'Grammar',
  },
  {
    type: 'multiple',
    id: 7,
    level: 'B1',
    skill: 'grammar',
    question: "She has been working here _____ 2015.",
    options: ['for', 'since', 'during', 'from'],
    correctAnswer: 1,
    points: 10,
    category: 'Grammar',
  },
  {
    type: 'multiple',
    id: 8,
    level: 'B1',
    skill: 'grammar',
    question: "Choose the correct form: 'I wish I _____ speak Chinese'",
    options: ['can', 'could', 'will', 'would'],
    correctAnswer: 1,
    points: 10,
    category: 'Grammar',
  },
  {
    type: 'multiple',
    id: 9,
    level: 'B1',
    skill: 'vocabulary',
    question: "What is a phrasal verb meaning 'to postpone'?",
    options: ['put off', 'put on', 'put up', 'put down'],
    correctAnswer: 0,
    points: 10,
    category: 'Vocabulary',
  },
  {
    type: 'multiple',
    id: 10,
    level: 'B1',
    skill: 'grammar',
    question: "By the time you arrive, I _____ dinner.",
    options: ['finish', 'will finish', 'will have finished', 'finished'],
    correctAnswer: 2,
    points: 10,
    category: 'Grammar',
  },
  {
    type: 'multiple',
    id: 11,
    level: 'B1',
    skill: 'grammar',
    question: "Choose the correct preposition: 'She is good ___ mathematics'",
    options: ['in', 'at', 'on', 'for'],
    correctAnswer: 1,
    points: 10,
    category: 'Grammar',
  },
  {
    type: 'multiple',
    id: 12,
    level: 'B1',
    skill: 'vocabulary',
    question: "What does 'break the ice' mean?",
    options: ['To destroy something', 'To start a conversation', 'To be very cold', 'To solve a problem'],
    correctAnswer: 1,
    points: 10,
    category: 'Vocabulary',
  },
  
  // Hard - Comprensión
  {
    type: 'multiple',
    id: 13,
    level: 'B2',
    skill: 'reading',
    question: "Reading: 'The invention of the steam engine revolutionized manufacturing, transforming small-scale craft production into large-scale industrial output. This shift fundamentally altered society by creating urban centers.' What was one major consequence?",
    options: ['It reduced the need for craftspeople', 'It led to the development of urban centers', 'It decreased overall wealth', 'It eliminated the need for factories'],
    correctAnswer: 1,
    points: 20,
    category: 'Reading',
  },
  {
    type: 'multiple',
    id: 14,
    level: 'B2',
    skill: 'grammar',
    question: "Which sentence uses subjunctive mood correctly?",
    options: ['I suggest that she comes early', 'I suggest that she come early', 'I suggest that she will come early', 'I suggest that she is coming early'],
    correctAnswer: 1,
    points: 20,
    category: 'Grammar',
  },
  {
    type: 'multiple',
    id: 15,
    level: 'B2',
    skill: 'vocabulary',
    question: "Choose the word that best completes: 'His _____ attitude made it difficult to work with him'",
    options: ['amenable', 'intractable', 'affable', 'gregarious'],
    correctAnswer: 1,
    points: 20,
    category: 'Vocabulary',
  },
  {
    type: 'multiple',
    id: 16,
    level: 'B2',
    skill: 'reading',
    question: "Reading: 'Despite the economic downturn, the company's revenue remained resilient, attributed largely to strategic diversification.' What helped the company?",
    options: ['Economic growth', 'Strategic diversification', 'Employee layoffs', 'Price increases'],
    correctAnswer: 1,
    points: 20,
    category: 'Reading',
  },
  {
    type: 'writing',
    id: 17,
    level: 'B2',
    skill: 'writing',
    question: "Describe your family in English.",
    prompt: "Write a short paragraph about your family. Include who they are and what they do.",
    points: 20,
    category: 'Writing',
  },
  {
    type: 'multiple',
    id: 18,
    level: 'B2',
    skill: 'vocabulary',
    question: "What does 'to beat around the bush' mean?",
    options: ['To be direct', 'To avoid the main topic', 'To work hard', 'To be confused'],
    correctAnswer: 1,
    points: 20,
    category: 'Vocabulary',
  },
  {
    id: 19,
    type: 'speaking',
    level: 'B1',
    skill: 'speaking',
    question: "Introduce yourself in English for 30 seconds.",
    prompt: "Introduce yourself in English for 30 seconds.",
    points: 15,
    category: 'Speaking',
  },
  {
    type: 'multiple',
    id: 20,
    level: 'B2',
    skill: 'grammar',
    question: "Complete: 'Scarcely _____ arrived when the meeting started'",
    options: ['I had', 'had I', 'I have', 'have I'],
    correctAnswer: 1,
    points: 20,
    category: 'Grammar',
  },
  {
    id: 25,
    level: 'A2',
    skill: 'listening',
    type: 'listening',
    category: 'Travel',
    question: 'Listen to the conversation and answer the question.',
    audio: {
      url: '/audio/A2/travel01.mp3',
      duration: 32,
    },
    options: ['By bus', 'By train', 'By taxi', 'On foot'],
    correctAnswer: 1,
    points: 5,
  },
  {
    id: 40,
    level: 'B1',
    skill: 'reading',
    type: 'reading',
    category: 'Environment',
    image: {
      url: '/images/forest.jpg',
      alt: 'Forest',
    },
    text: 'Look at the image and read the paragraph below.',
    question: 'What is the main problem described?',
    options: ['Pollution', 'Deforestation', 'Flooding', 'Traffic'],
    correctAnswer: 1,
    points: 5,
  },
  {
    id: 60,
    level: 'B2',
    skill: 'speaking',
    type: 'speaking',
    category: 'Personal',
    question: 'Describe your favorite vacation.',
    prompt: 'Speak for about one minute. Mention where you went, what you did and why you liked it.',
    timeLimit: 60,
    points: 10,
  },
  {
    id: 70,
    level: 'C1',
    skill: 'writing',
    type: 'writing',
    category: 'Formal Email',
    question: 'Write an email requesting information about a university program.',
    prompt: 'Write between 150 and 200 words.',
    timeLimit: 900,
    points: 15,
  },
];

export const getLevelFromScore = (score: number): { level: string; description: string; message: string } => {
  if (score >= 91) return { level: 'C2', description: 'Maestría - Dominio completo', message: '¡Perfectamente! Eres prácticamente bilingüe' };
  if (score >= 76) return { level: 'C1', description: 'Avanzado - Muy dominado', message: '¡Muy bien! Dominas muy bien' };
  if (score >= 56) return { level: 'B2', description: 'Intermedio-Alto - Competente', message: '¡Excelente! Nivel competente' };
  if (score >= 36) return { level: 'B1', description: 'Intermedio - Desarrollo', message: '¡Vas bien! Continúa mejorando' };
  if (score >= 21) return { level: 'A2', description: 'Elemental - Bajo', message: 'Buen inicio, sigue practicando' };
  return { level: 'A1', description: 'Principiante - Muy básico', message: 'Necesitas más práctica fundamental' };
};
