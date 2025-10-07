import { Check } from "lucide-react";

export default function ProgressIndicator({ steps, currentStep }) {
  return (
    <div className="progress-indicator">
      {steps.map((step, index) => {
        const Icon = step.icon;
        const isCompleted = step.id < currentStep;
        const isCurrent = step.id === currentStep;
        
        return (
          <div key={step.id} className="progress-step">
            <div className={`step-circle ${isCompleted ? 'completed' : ''} ${isCurrent ? 'current' : ''}`}>
              {isCompleted ? (
                <Check size={16} />
              ) : (
                <Icon size={16} />
              )}
            </div>
            <span className={`step-title ${isCurrent ? 'current' : ''}`}>
              {step.title}
            </span>
            {index < steps.length - 1 && (
              <div className={`step-connector ${isCompleted ? 'completed' : ''}`} />
            )}
          </div>
        );
      })}
    </div>
  );
}
