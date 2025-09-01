import App from "@/components/App";
import { env } from "@/lib/env";
import { Metadata } from "next";

const appUrl = env.NEXT_PUBLIC_URL;

const frame = {
  version: "next",
  imageUrl: `${appUrl}/images/feed.png`,
  button: {
    title: "Launch Kinic",
    action: {
      type: "launch_frame",
      name: "Kinic AI Memory",
      url: appUrl,
      splashImageUrl: `${appUrl}/images/splash.png`,
      splashBackgroundColor: "#3b82f6",
    },
  },
};

export async function generateMetadata(): Promise<Metadata> {
  return {
    title: "Kinic AI Memory",
    openGraph: {
      title: "Kinic AI Memory",
      description: "AI memory and collaboration platform on Base blockchain",
    },
    other: {
      "fc:frame": JSON.stringify(frame),
    },
  };
}

export default function Home() {
  return <App />;
}
