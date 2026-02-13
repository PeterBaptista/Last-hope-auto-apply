import { CollectionConfig } from 'payload'

export const JobVacancies: CollectionConfig = {
  slug: 'job-vacancies',
  admin: {
    useAsTitle: 'title',
  },
  access: {
    create: () => true, // Open for now to allow microservice to post easily
    read: () => true,
  },
  fields: [
    {
      name: 'title',
      type: 'text',
      required: true,
    },
    {
      name: 'company',
      type: 'text',
    },
    {
      name: 'location',
      type: 'text',
    },
    {
      name: 'description',
      type: 'richText',
    },
    {
      name: 'applicationLink',
      type: 'text',
    },
    {
      name: 'postedDate',
      type: 'date',
    },
    {
      name: 'source',
      type: 'text',
    },
    {
      name: 'scrapedAt',
      type: 'date',
      defaultValue: () => new Date().toISOString(),
    },
  ],
}
