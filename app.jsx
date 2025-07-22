import React, { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const quizData = [
  {
    question: "Which of the following is *not* mentioned as an example of a successful application of deep learning?",
    options: [
      "Speech recognition",
      "Spam detection",
      "Legal document drafting",
      "Image classification",
    ],
    answer: "Legal document drafting",
  },
  {
    question: "Deep learning solves problems by explicitly programming all the necessary rules a system needs to follow.",
    options: ["True", "False"],
    answer: "False",
  },
  {
    question: "A deep learning model learns to represent data through a ___________ of concepts, each defined in terms of simpler concepts.",
    options: ["chain", "web", "hierarchy", "collection"],
    answer: "hierarchy",
  },
  {
    question: "Why did early AI systems like Cyc struggle to generalize and succeed in real-world environments?",
    options: [
      "They lacked enough data",
      "They were too expensive to operate",
      "They relied on hard-coded formal knowledge that couldn't capture intuitive and informal real-world information",
      "They were using outdated hardware"
    ],
    answer: "They relied on hard-coded formal knowledge that couldn't capture intuitive and informal real-world information",
  },
  {
    question: "What is the main advantage of using representation learning?",
    options: [
      "Reduces need for GPUs",
      "Allows models to find meaningful features automatically",
      "Simplifies the software engineering process",
      "Makes models faster but less accurate"
    ],
    answer: "Allows models to find meaningful features automatically",
  },
];

export default function DeepLearningQuiz() {
  const [current, setCurrent] = useState(0);
  const [selected, setSelected] = useState(null);
  const [score, setScore] = useState(0);
  const [completed, setCompleted] = useState(false);

  const handleSelect = (option) => {
    setSelected(option);
  };

  const handleNext = () => {
    if (selected === quizData[current].answer) {
      setScore(score + 1);
    }
    if (current + 1 < quizData.length) {
      setCurrent(current + 1);
      setSelected(null);
    } else {
      setCompleted(true);
    }
  };

  return (
    <div className="max-w-xl mx-auto p-4 space-y-4">
      {completed ? (
        <Card>
          <CardContent className="text-center p-6">
            <h2 className="text-2xl font-bold">Quiz Completed!</h2>
            <p className="mt-2">You scored {score} out of {quizData.length}.</p>
          </CardContent>
        </Card>
      ) : (
        <Card>
          <CardContent className="p-6 space-y-4">
            <h2 className="text-lg font-semibold">
              Question {current + 1} of {quizData.length}
            </h2>
            <p className="text-md">{quizData[current].question}</p>
            <div className="space-y-2">
              {quizData[current].options.map((option) => (
                <Button
                  key={option}
                  variant={selected === option ? "default" : "outline"}
                  onClick={() => handleSelect(option)}
                  className="w-full text-left"
                >
                  {option}
                </Button>
              ))}
            </div>
            <Button onClick={handleNext} disabled={!selected} className="mt-4 w-full">
              {current + 1 === quizData.length ? "Finish" : "Next"}
            </Button>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
