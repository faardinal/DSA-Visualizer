import { toast as sonnerToast } from "sonner";

export function toast({ title, description, variant } = {}) {
  const message = title || description || "";
  const options = description && title ? { description } : undefined;

  if (variant === "destructive") {
    return sonnerToast.error(message, options);
  }

  return sonnerToast(message, options);
}

export { sonnerToast as dismissToast };
