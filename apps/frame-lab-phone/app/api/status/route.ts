import { getApiKey, getBaseHost, getModel } from "@/lib/config";
import { getSearchProvider } from "@/lib/search";

export const dynamic = "force-dynamic";

export async function GET() {
  return Response.json({
    live: Boolean(getApiKey()),
    model: getApiKey() ? getModel() : "frame-lab-mock",
    baseHost: getBaseHost(),
    searchProvider: getSearchProvider(),
  });
}
