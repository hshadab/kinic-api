"use client";

import { MiniAppProvider } from "@/contexts/miniapp-context";
import { env } from "@/lib/env";
import { MiniKitProvider } from "@coinbase/onchainkit/minikit";
import dynamic from "next/dynamic";
import { base } from "viem/chains";

const ErudaProvider = dynamic(
  () => import("../components/Eruda").then((c) => c.ErudaProvider),
  { ssr: false }
);

export default function Providers({ children }: { children: React.ReactNode }) {
  return (
    <ErudaProvider>
      <MiniKitProvider
        projectId={env.NEXT_PUBLIC_MINIKIT_PROJECT_ID}
        notificationProxyUrl="/api/notification"
        chain={base}
      >
        <MiniAppProvider>{children}</MiniAppProvider>
      </MiniKitProvider>
    </ErudaProvider>
  );
}
